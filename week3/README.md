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
SELECT  FROM `bigquery-public-data.new_york_citibike.citibike_stations` LIMIT 1000
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

