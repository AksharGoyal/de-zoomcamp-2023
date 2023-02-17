# Theory  

## OLTP vs OLAP  

Here is an overview of what is OnLine Transaction Processing and OnLine Analytical Processing.

|   |  OLTP |  OLAP |
| :--- |    :---   | :--- |
| Purpose | OLTP databases are used when we want to group a couple of SQL queries together and you want to fall back or roll back in case one of them falls       | OLAP is used for data ingestion and discovering hidden insights (used for analytical purposes hence the name) |
| Data Updates | Updates are fast but small | data is periodically refreshed and larger in comparison to OLTP |
| Database Design | Normalized database for efficiency | Denormalized database for analysis |
| Data View | Lists daily business transactions | Multi-dimensional view of enterprise data |
| Space requirements | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| Productivity | Productivity is increased for the end users | Productivity increases for business managers, data analysts, and executives |
| User examples | Customer-facing personnel, online shoppers | Knowledge workers such as data analysts, business analysts and executives |
| Backup and Recovery | Regular backups required to ensure business continuity and meet legal requirements | Lost data can be reloaded from OLTP as need in place of regular backups |
  
  
## Data Warehouse

Data Warehouse falls in OLAP category used for reporting and data analysis. It consists of raw data, metadata and summary. It has many data sources such as OS, flat files, OLTP database, etc. Data Warehouse can be transformed into Data Marts (subsets of Data Warehouse) which different users can access. Data Scientist can use raw data from Data Warehouse.  

<img width="90%" alt="image" src="https://user-images.githubusercontent.com/38995624/219380978-ae91f697-bb48-4649-860e-5f85266a936b.png">

## BigQuery  

BigQuery is a Data Warehouse sans server to manage or database software to install. BigQuery provides software as well as infrastructure including scalability and high availability. One can start with couple of gigabytes in BigQuery and can scale easily to petabytes easily. We can do machine learning via SQL interface in BigQuery, handle geospatial data and doing business intelligence queries. BigQuery maximizes flexibility by separating compute engine that analyzes your data from your storage.

## BigQuery Interface  

<img width="958" alt="image" src="https://user-images.githubusercontent.com/38995624/219385431-200726c6-4ff4-49f1-abea-44a401097c97.png">

Here, `dtc-de-akshar` is the project name, `nyc_taxi` is the dataset and the tables inside are external. BigQuery provides a lot of open-source public data. For example, we can run the following command in which the dataset can be accessed by anyone and we can also see its schema, preview or other details.
```sql
SELECT FROM `bigquery-public-data.new_york_citibike.citibike_stations` LIMIT 1000
```
The results can be explored through Data Studio and the query results can be saved as a CSV file too.  

## BigQuery Costs  

- On demand pricing:  
  - 1 TB of data processed is $5  
- Flat rate pricing  
  - Based on number of pre requested slots  
  - 100 slots $\rightarrow$ \$2k/month = 400 TB data processed on demand pricing  

Flat rate pricing is not recommended unless we are scanning 200TB of data. On demand pricing is also preferred if we running N+1 queries and our N slots are full so the (N+1)$^{th}$ query will have to wait in Flate rate pricing. On demand BigQuery can give us more slots as per the requirements of the query.

## External Tables  

We can cretae external tables from datasets in your bucket. Here I am using all the 24 parquet files of yellow trip data of 2019 and 2020. 
```sql
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-akshar.nyc_taxi.external_yellow_nytaxi`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bigquery_dtc_de_week_3/data/yellow/yellow_tripdata_2019-*.parquet', 'gs://bigquery_dtc_de_week_3/data/yellow/yellow_tripdata_2020-*.parquet']
);
```
External Tables have 0 storage size and 0 tabel size. However it cannot tell us the number of rows the table has as the table is not stored inside BigQuery.  

## Partioning  

When writing a query, we use one or more columns for filtering our datasets. We can partition the table to improve the performance and thus, retrieve information faster without reading any other records where the paritioning column doesn't meet the filter condition. In the comments of provided `bigquery_practice.sql` file in Practice folder, we observe that partitioning reduces cost and speed which implies improvement in performance whilge getting us the same results as for the non-partitioned table.
```sql
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
```

We can also see which partition has how many rows.
```sql
SELECT table_name, partition_id, total_rows
FROM `nyc_taxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;
```
<img width="416" alt="image" src="https://user-images.githubusercontent.com/38995624/219594221-39cd4c9e-a47f-44af-a884-3f3141e39863.png">

## Clustering  

We can cluster tables too by clustering on a column to group same tags which can improve our cost as well as query performance.  
```sql
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
-- PROCESSED 880.27MB in 693m
```

We can specify maximum of 4000 partitions and specify upto 4 clustering columns. Clustering columns must be top-level, non-repeated:  
- DATE  
- BOOL
- GEOGRAPHY
- INT64
- NUMERIC
- BIGNUMERIC
- STRING
- TIMESTAMP
- DATETIME

## Partitioning vs Clustering  

| Clustering | Partitioning |  
| :--- | :--- |  
| Cost Benefit unknown | Cost known upfront (helpful in maintaining queries in particular amount of cost) |  
| Provides more granularities | Need partition-level management only (deleting or creating new partitions between storage which is not possible in clustering) |  
| Filter or aggregate on multiple column | Partioning can be done only on one column so our queries will filter or aggregate on single column |  
| Cardinality of number of values in a column or group of columns is large | There is a limitation of 4000 partitions |  

Use clustering if  
- Partitioning results in small amount of data per partition ( $<1$ GB ) hence clustering is preferred for small partitions or high granularity in a column
- number of partitions is large ( $>4000$ )
- Querying every hour or writing data to BigQuery every hour can modify partitions which is not a good idea.

## BigQuery Best Practices  

- Cost reduction  
  - Avoid SELECT \*, only use the columns that are needed to reduce cost of reading
  - Price your queries before running them (highlighting a query can show an estimated cost of running it)
  - use clustered or partitioned table for improved performance
  - Use streaming inserts with caution (streaming can increase costs hence it is asked to avoid streaming in the homework)
  - Materialize query results in stages
  - Filter on partitioned columns
  - Denormalize data
  - Use nested or repeated columns
  - Use external data sources appropriately
  - Reduce data before using JSON
  - Do not treat WITH clauses as prepared statements
  - Avoid oversharding (over-partitioning) tables
  - Order last to optimize performance

