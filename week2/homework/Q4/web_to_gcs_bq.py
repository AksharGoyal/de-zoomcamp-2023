from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("akshar-zoom-prefect-gcs")
    gcs_block.upload_from_path(from_path=path.as_posix(), to_path=path)
    return

@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    # Path(f"data/{color}").mkdir(parents=True, exist_ok=True, mode=0o755)
    # path = Path(f"data/{color}/{dataset_file}.parquet")
    # df.to_parquet(path, compression="gzip", index=False)
    # return path
    def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path_file = f"{dataset_file}.parquet"
    path_dir = Path(f"data/{color}")
    path_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path_dir / path_file, compression="gzip")
    return path_dir / path_file

@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    # df_clean = clean(df)
    path = write_local(df, color, dataset_file)
    write_gcs(path)

@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("akshar-zoom-prefect-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"./{gcs_path}").as_posix()


# @task()
# def transform(path: Path) -> pd.DataFrame:
#     """Data cleaning example"""
#     df = pd.read_parquet(path)
#     print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
#     df["passenger_count"].fillna(0, inplace=True)
#     print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
#     return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("akshar-zoom-gcp-creds")

    df.to_gbq(
        destination_table="zoomcamp_akshar_prefect.yellow_2019_02_03",
        project_id="dtc-de-akshar",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow(log_prints=True)
def etl_gcs_to_bq(
    months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"
):
    """Main ETL flow to load data into Big Query"""
    num_rows = 0
    for month in months:
        etl_web_to_gcs(year, month, color)
        # print("etl_web_to_gcs Done!\n")
        path = extract_from_gcs(color, year, month)
        # print(f"Path defined Done!: {path}\n")
        df = pd.read_parquet(path)
        # print("Read the parquet file\n")
        # print(df.columns)
        # print(df.dtypes)
        # print(df.head(2))
        # print("Info reading Done!\n")
        num_rows += df.shape[0]
        # print(f"Number of rows: {num_rows}")
        # print("Writing to BQ now...\n")
        write_bq(df)
        # print("Writing to BQ Done!\n")
    print(f"Total number of rows: {num_rows}")

if __name__ == "__main__":
    color = "yellow"
    year = 2021
    months = [1,2,3]
    etl_gcs_to_bq(months, year, color)
