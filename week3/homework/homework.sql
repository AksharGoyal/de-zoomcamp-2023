-- QUESTION 1
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-akshar.nyc_taxi.fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bigquery_dtc_de_week_3/data/fhv/fhv_tripdata_2019-*.csv.gz']
);

SELECT count(pickup_datetime) FROM `dtc-de-akshar.nyc_taxi.fhv_tripdata`;
-- 43,244,696

-- QUESTION 2
-- EXT TABLE
SELECT COUNT(DISTINCT(dispatching_base_num)) FROM `dtc-de-akshar.nyc_taxi.fhv_tripdata`;
-- NATIVE TABLE
SELECT COUNT(DISTINCT(dispatching_base_num)) FROM `dtc-de-akshar.fhv_data.fhv_tripdata`;
-- 0 MB for the External Table and 317.94MB for the Materialized Tabl

-- QUESTION 3
SELECT COUNT(1) FROM dtc-de-akshar.nyc_taxi.fhv_tripdata where DOlocationID is null and PUlocationID is null;
-- 717,748

-- QUESTION 4
CREATE OR REPLACE TABLE `dtc-de-akshar.nyc_taxi.fhv_partitioned_tripdata`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS (
  SELECT * FROM `dtc-de-akshar.fhv_data.fhv_tripdata`);
-- Partition by pickup_datetime Cluster on affiliated_base_number

-- question 5
SELECT DISTINCT(affiliated_base_number) FROM `dtc-de-akshar.fhv_data.fhv_tripdata`
WHERE pickup_datetime BETWEEN '2019-01-01' AND '2019-03-31';
SELECT DISTINCT(affiliated_base_number) FROM `dtc-de-akshar.nyc_taxi.fhv_partitioned_tripdata`
WHERE pickup_datetime BETWEEN '2019-01-01' AND '2019-03-31';
-- 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table
