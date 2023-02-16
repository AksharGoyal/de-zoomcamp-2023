-- CREATING AN EXTERNAL TABLE
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-akshar.nyc_taxi.external_yellow_nytaxi`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bigquery_dtc_de_week_3/data/yellow/yellow_tripdata_2019-*.parquet', 'gs://bigquery_dtc_de_week_3/data/yellow/yellow_tripdata_2020-*.parquet']
);

-- SEEING PERFORMANCE OF AN EXTERNAL TABLE
SELECT * FROM dtc-de-akshar.nyc_taxi.external_yellow_nytaxi limit 10;

CREATE OR REPLACE TABLE dtc-de-akshar.nyc_taxi.yellow_tripdata_non_partitoned AS
SELECT * FROM dtc-de-akshar.nyc_taxi.external_yellow_nytaxi;

-- CREATING A PARTITIONED TABLE
CREATE OR REPLACE TABLE dtc-de-akshar.nyc_taxi.yellow_tripdata_partitoned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM dtc-de-akshar.nyc_taxi.external_yellow_nytaxi;

-- COMPARING PERFORMANCE OF PARTITIONED AND NON-PARTITIONED TABLE
SELECT DISTINCT(VendorID)
FROM dtc-de-akshar.nyc_taxi.yellow_tripdata_non_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
-- PROCESSED 1.62 GB IN 731ms
SELECT DISTINCT(VendorID)
FROM dtc-de-akshar.nyc_taxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
-- PROCESSED 105.91 MB in 467ms

-- GETTING INFORMATION ABOUT THE PARTITIONS IN THE PARTITIONED TABLE
SELECT table_name, partition_id, total_rows
FROM `nyc_taxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;

-- CREATING A CLUSTERED TABLE
CREATE OR REPLACE TABLE dtc-de-akshar.nyc_taxi.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM dtc-de-akshar.nyc_taxi.external_yellow_nytaxi;

-- USE OF PARTIONING
SELECT count(*) as trips
FROM dtc-de-akshar.nyc_taxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
-- PROCESSED 1.07GB in 731ms

-- USE OF CLUSTERING
SELECT count(*) as trips
FROM dtc-de-akshar.nyc_taxi.yellow_tripdata_partitoned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
-- PROCESSED 880.27MB in 693ms
