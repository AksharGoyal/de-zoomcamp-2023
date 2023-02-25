{{ config(materialized='view') }}

select count(*) as number_of_records from {{ ref('fact_trips') }}
where date(pickup_datetime) between date('2019-01-01') and date('2020-12-31')
