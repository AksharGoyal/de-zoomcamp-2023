# DBT  

## Analytical Engineering  

So far we learnt that warehouses like BigQuery, Snowflake or Redshift help in reducing the cost of storage in computing. In a data team, we have a Data Engineer and a Data Analyst. The DE prepares and maintains the infrastructure the data team needs whereas the DA uses the data hosted in that infrastructure to answer questions and solves problems. The modern Data Analysts are writing more code but don't have expertise in software engineering; this is not their first priority. Data Engineers are great software engineers but don't know how to use the data is useful for the people in business.  

The Analytical Engineers come here to fill in this gap. they introduce good software engineering practices to the efforts of data analysts and data engineers. AE uses tools that was used for loading (such as Stitch or PipeRider), storing (BigQuery, Snowflake), modelling (dbt, dataform) and finally presentation (Tableau, Looker, Data Studio). AE is more of an ELT approach as we have the data loaded so we it provides faster and more flexible data analysis. Also, the data cloud warehousing lowers the cost of storage and computing so we can load all of the data and transform it in same warehouse.

# Homework  

The models created such as `stf_fhv_tripdata` and `fact_fhv_trips` can be found in models directory <a href="https://github.com/AksharGoyal/de-zoomcamp-2023/tree/main/week4/models">models</a>, particularly the commands to check count in homework directory. Solutions for the multiple choice can be found in <a href="https://github.com/AksharGoyal/de-zoomcamp-2023/blob/main/week4/homework.md">homework.md</a>.
