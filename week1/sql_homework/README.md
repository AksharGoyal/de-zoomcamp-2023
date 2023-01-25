The files needed for the homework can be obtained through:  
 - `wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz`  
 - `wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv`

The command I used for ingesting the data first time is
```bash
docker run -it --network=homework_default  taxi_ingest:v001  
--user=root  --password=root  --host=pgdatabase  --port=5432  
--db=ny_taxi  --table_name=taxi_zone_lookup     --url=${URL}
```
where `URL` is any of the links to the dataset and homework is name of the folder for my files hence the netowk name is `homework_default`.  
Note: everytime you make a change to `ingest_data.py` file, make sure to build the Dockerfile again else it will give errors.
