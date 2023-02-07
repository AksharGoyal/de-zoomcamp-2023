from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("akshar-zoom-prefect-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"./{gcs_path}")


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
        destination_table="zoomcamp_akshar_prefect.rides",
        project_id="dtc-de-akshar",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow(print_logs=True)
def etl_gcs_to_bq(
    months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"
):
    """Main ETL flow to load data into Big Query"""
    num_rows = 0
    for month in months:
        path = extract_from_gcs(color, year, month)
        # df = transform(path)
        df = pd.read_parquet(path)
        num_rows += df.shape[0]
        write_bq(df)


if __name__ == "__main__":
    color = "yellow"
    year = 2021
    months = [1,2,3]
    etl_gcs_to_bq(months, year, color)
