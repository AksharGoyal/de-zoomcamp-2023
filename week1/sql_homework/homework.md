# Data Engineering Zoomcamp Homework 1 2023

## Question 1  

When we run `docker build`, we get the following output:  

```bash
$ docker build
"docker build" requires exactly 1 argument.
See 'docker build --help'.

Usage:  docker build [OPTIONS] PATH | URL | -

Build an image from a Dockerfile
(base)
```    

Then we run `docker build --help` to see:
```bash
$ docker build --help

Usage:  docker build [OPTIONS] PATH | URL | -

Build an image from a Dockerfile

Options:
      .
      .
      .
      --iidfile string          Write the image ID to the file
```
We see the answer so we choose the option `--iidfile string`.

## Question 2  

we run the command `docker run-it --entrypoint=bash python:3.9` to get the following output:
```
pip list
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```
We see there are 3 modules packages installed so we choose the option 3.

The following questions are related to SQL and answered using pgAdmin's Query Editor.

## Question 3  

Here, we use the date function to get only the date parts of pickup and dropoff dates. We look for the trips with same pickup and dropoff dates which is 15th Jan 2019 and arrive to the answer: **20530**

```sql
select count(*) from green_taxi_trips
where date(lpep_pickup_datetime)=date(lpep_dropoff_datetime) and
date(lpep_pickup_datetime)='2019-01-15'
```
<!-- <img width="150" height="!50" alt="image" src="https://user-images.githubusercontent.com/38995624/214545424-c0df75b2-a059-44c5-b96d-618fefd9e34d.png"> -->
  
|    | count  |  
| ------------- |:-------------:| 
| 1     | 20530 |  

## Question 4  

For this question, we will use GroupBy and Max aggregate function as well as alias to get to the answer: **2019-01-15**.
```sql
select date(lpep_pickup_datetime) as pickupDate, max(trip_distance) as maxDistanceTrip from green_taxi_trips
group by pickupDate
order by maxDistanceTrip desc
```  
|    | pickupdate  |  maxdistancetrip  |  
| ------------- |:-------------:|:-------------:| 
| **1** | **2019-01-15** | **117.99** |  
| 2 | 2019-01-18 | 80.96 |  
| $\vdots$ | | |  

<!-- <img width="250" height="200" alt="image" src="https://user-images.githubusercontent.com/38995624/214547512-19bebe30-75d8-42d7-9779-e21e7afae94a.png"> -->

## Question 5

In this question, we use groupby to get the count of trips on 1st Jan 2019 grouped by number of passengers. We use where clause to specify the date and additionally passenger_count (for the sake of display).

```sql
select passenger_count, count(date(lpep_pickup_datetime)) as tripCount from green_taxi_trips
where date(lpep_pickup_datetime)='2019-01-01' and passenger_count in (2,3)
group by passenger_count
```
|    | passenger_count  |  tripcount  |  
| ------------- |:-------------:|:-------------:| 
| 1 | 2 | 1282 |  
| 2 | 3 | 254 |  

<!-- <img width="200" height="100" alt="image" src="https://user-images.githubusercontent.com/38995624/214548045-44feb496-17a9-48a4-9169-f248f3a59a09.png"> -->

## Question 6  

This question takes your SQL on a higher level as this requires you to use JOIN.
```sql
select tzldo."Zone", max(tip_amount) as maxTip from green_taxi_trips gtt join taxi_zone_lookup tzl on tzl."LocationID" = gtt."PULocationID"
join taxi_zone_lookup tzldo on tzldo."LocationID" = gtt."DOLocationID"
where tzl."Zone" = 'Astoria' and tzldo."Zone" is not null
group by tzldo."Zone"
order by tip desc;
```
|    | Zone  |  maxtip  |  
| ------------- |:-------------:|:-------------:|  
| **1** | **Long Island City/Queens Plaza** | **88** |  
| 2 | Central Park | 30 |  
| 3 | Jamaica | 25 |  
| $\vdots$ | | |
