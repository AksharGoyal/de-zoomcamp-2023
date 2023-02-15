# Solution to DEzoomcamp Week 3 homework  

## Question 1: What is count for fhv vehicle records for year 2019?  
- 43,244,696

## Question 2: What is the estimated amount of data that will be read when you execute your query on the External Table and the Materialized Table?  
- 0 MB for the External Table and 317.94MB for the Materialized Table

## Question 3: How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
- 717,748

## Question 4: What is the best strategy to make an optimized table in Big Query if your query will always filter by pickup_datetime and order by affiliated_base_number?  
- Partition by pickup_datetime Cluster on affiliated_base_number

## Question 5:  
Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 
03/01/2019 and 03/31/2019 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? 

Choose the answer which most closely matches:
- 47.87 MB for non-partitioned table and 23.06 MB for the partitioned table

## Question 6: Where is the data stored in the External Table you created?  
- Big Query

## Question 7: It is best practice in Big Query to always cluster your data.  
- False  
