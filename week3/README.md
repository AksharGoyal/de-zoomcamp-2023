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
