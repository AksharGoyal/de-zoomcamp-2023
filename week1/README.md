# DE Zoomcamp 2023: The beginning  

For this zoomcamp, I am using Windows and Git Bash. Note that files used may be slightly different from the ones provided from the zoomcamp themselves so make sure to use those ones first.

## How to use the files:  

 - Make a folder and have the the 3 files: Dockerfile, docker-compose.yaml and ingest_data.py.  
 - Get the data through `URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"`. Note that it can be in csv or parquet format too and that's fine. In the end, we need to provide data to work on. But make sure wget works on your terminal!
 - Make sure to run `docker build -t taxi_ingest:v001 .` so that the container knows to use recently updated files (ingest_data.py) in this case.  
 - If you are using the docker-compose.yaml from my repo, create a directory called data_pgadmin to persist the data there.
 - Run `docker-compose up`. I prefer running `docker-compose up -d` as it allows me to run other commands in the same terminal. By not detaching it, I have to open a separate terminal to run commands.
 - If you are ingesting the data for the first time, you will want to run the command:  
 ```bash
    docker run -it --network=week_1_basics_n_setup__default  taxi_ingest:v001  
    --user=root  --password=root  --host=pgdatabase  --port=5432  
    --db=ny_taxi  --table_name=taxi_zone_lookup     --url=${URL}
 ```
 
   The arguements for `--network` and `--host` can differ based on how you name your folder (that's how the created network's name comes from) and how you name your host for postgres.
