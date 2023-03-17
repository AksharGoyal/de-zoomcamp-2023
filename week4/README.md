# DBT  

## Analytical Engineering  

So far we learnt that warehouses like BigQuery, Snowflake or Redshift help in reducing the cost of storage in computing. In a data team, we have a Data Engineer and a Data Analyst. The DE prepares and maintains the infrastructure the data team needs whereas the DA uses the data hosted in that infrastructure to answer questions and solves problems. The modern Data Analysts are writing more code but don't have expertise in software engineering; this is not their first priority. Data Engineers are great software engineers but don't know how to use the data is useful for the people in business.  

$\underline{\text{About Analytical Engineering:}}$ The Analytical Engineers come here to fill in this gap. they introduce good software engineering practices to the efforts of data analysts and data engineers. AE uses tools that was used for loading (such as Stitch or PipeRider), storing (BigQuery, Snowflake), modelling (dbt, dataform) and finally presentation (Tableau, Looker, Data Studio). AE is more of an ELT approach as we have the data loaded so we it provides faster and more flexible data analysis. Also, the data cloud warehousing lowers the cost of storage and computing so we can load all of the data and transform it in same warehouse.  

$\underline{\text{Kimball's Dimensional Modeling:}}$ The objective is to deliver data that is understandable to business users but also deliver fast query performance. Similar to 3NF, we can sacrifice non-redundancy to prioritise user understandability and query performance.  

$\underline{\text{Elements of Dimensional Modeling:}}$ The Star Schema consists of Fact tables and Dimension tables.  
- Fact tables are going to be the measurement metrics or just facts about business. They correspond to a business process, like sales or orders.  
- Dimension tables provide context to facts tables; they correspond to a business identity.
- Fact tables can be thought as verbs and Dimension tables can be thought as nouns.

<img width="300" alt="image" style="text-align: center;" src="https://user-images.githubusercontent.com/38995624/225933463-3a2fc25f-0d97-4c48-9978-3b1b3e5b8724.png">

$\underline{\text{Architecture of Dimensional Modeling:}}$  
- **Stage Area:** We have raw data not exposed to anyone but only those who know how to use it.  
- **Processing area:** We take the raw data and make data models out of them. Again, it's not exposed to everyone. The engineers focus in efficiency and ensure the standards are being followed.  
- **Presentation Area:** This is presentation of data exposed to business stakeholders 

# Homework  

The models created such as `stv_fhv_tripdata` and `fact_fhv_trips` can be found in models directory <a href="https://github.com/AksharGoyal/de-zoomcamp-2023/tree/main/week4/models">models</a>, particularly the commands to check count in homework directory. Solutions for the multiple choice can be found in <a href="https://github.com/AksharGoyal/de-zoomcamp-2023/blob/main/week4/homework.md">homework.md</a>.
