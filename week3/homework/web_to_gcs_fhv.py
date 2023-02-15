from pathlib import Path
import modin.pandas as pd
import pandas
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
# from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta
import ray
ray.init(runtime_env={'env_vars': {'__MODIN_AUTOIMPORT_PANDAS__': '1'}})

# import pyarrow.csv as pv
# import pyarrow.parquet as pq
# import pyarrow as pa

# dtypes_yellow = dict([
#         ('VendorID', 'object'),
#         ('lpep_pickup_datetime',"datetime64"),
#         ('lpep_dropoff_datetime',"datetime64"),
#         ('store_and_fwd_flag','object'),
#         ('RatecodeID', 'int64'),
#         ('PULocationID','int64'),
#         ('DOLocationID','int64'),
#         ('passenger_count','int64'),
#         ('trip_distance','float64'),
#         ('fare_amount','float64'),
#         ('extra','float64'),
#         ('mta_tax','float64'),
#         ('tip_amount','float64'),
#         ('tolls_amount','float64'),
#         ('ehail_fee','float64'),
#         ('improvement_surcharge','float64'),
#         ('total_amount','float64'),
#         ('payment_type','int64'),
#         ('trip_type','int64'),
#         ('congestion_surcharge','float64')]
# )
# print(dtypes_yellow)
@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str, color: str='yellow') -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url, compression='gzip')
    print("URL:",dataset_url,'\n')
    print("Inside Fetch:\n", df.shape)
    # print(df.isna().sum())
    # df = df.loc[~df.VendorID.isna()]
    return df

@task(log_prints=True)
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    path = path.as_posix()
    gcs_block = GcsBucket.load("week3-bigquery-akshar")
    gcs_block.upload_from_path(from_path=path, to_path=path, timeout=360)
    return

@task(log_prints=True)
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path_dir = Path(f"data/{color}")
    path_dir.mkdir(parents=True, exist_ok=True)
    path_file = f"{dataset_file}.csv.gz"
    df.to_csv(path_dir / path_file, compression="gzip", index=False)
    # path_file = f"{dataset_file}.csv"
    # df.to_csv(path_dir / path_file, compression="gzip", index=False)
    # path_file = f"{dataset_file}.parquet"
    # df.to_parquet(path_dir / path_file, index=False, compression="gzip")
    # print("Inside write_local:\n", path_dir / path_file)
    # return path_dir / path_file

@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url, color)
    df_clean = transform(df, color)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)

@task(log_prints=True)
def transform(df: pd.DataFrame, color: str = 'yellow') -> pd.DataFrame:
    """Data cleaning example"""
    # newdf = df.select_dtypes(include='number')
    # for col in newdf.columns:
    #     df[col].fillna(0, inplace=True)
    # df['VendorID'] = df['VendorID'].astype('int64')
    # df['PUlocationID'] = df['PUlocationID'].astype('Int64')
    # df['RatecodeID'] = df['RatecodeID'].astype('int64')
    # df['DOlocationID'] = df['DOlocationID'].astype('Int64')
    # df['passenger_count'] = df['passenger_count'].astype('int64')
    # df['payment_type'] = df['payment_type'].astype('int64')
    # if color == 'yellow':
    #     # df['VendorID'] = df['VendorID'].astype('int64')
    #     df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    #     df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    # if color == 'green':
    #     df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    #     df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    # print("Number of rows after cleaning:", df.shape)
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropOff_datetime'] = pd.to_datetime(df['dropOff_datetime'])
    # df['SR_Flag'] = df['SR_Flag'].astype('Int64')
    return df


@flow(log_prints=True)
def etl_web_to_gcs_main(
    months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"
):
    """Main ETL flow to load data into Big Query"""
    for month in months:
        # etl_web_to_gcs(year, month, color)
        dataset_file = f"{color}_tripdata_{year}-{month:02}"
        dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{color}_tripdata_2019-01.csv.gz"
        df = fetch(dataset_url, color)
        # print(df.info())
        # print(df.isna().sum())
        # write_local(df, color, dataset_file)
        print("File downloading Done!\n")
        path_dir = Path(f"data/{color}")
        path_dir.mkdir(parents=True, exist_ok=True)
        dataset_file = f"{color}_tripdata_{year}-{month:02}"
        path_file = f"{dataset_file}.csv.gz"
        print("BEGIN:", path_dir / path_file)
        # df = pd.read_csv(path_dir / path_file, compression='gzip')
        dfnew = transform(df, color)
        # path_file = f"{dataset_file}.parquet"
        # dfnew.to_parquet(path_dir / path_file, index=False)
        dfnew.to_csv(path_dir / path_file, compression='gzip', index=False)
        write_gcs(path_dir / path_file)
        print("DONE:", path_dir / path_file, '\n')

if __name__ == "__main__":
    color = "fhv"
    year = 2019
    months = [i for i in range(1,13)]
    etl_web_to_gcs_main(months, year, color)
    # year = 2020
    # etl_gcs_to_bq(months, year, color)
