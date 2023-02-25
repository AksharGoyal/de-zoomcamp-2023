{{ config(materialized='view') }}

select count(*) as number_of_records from {{ ref('fact_fhv_trips') }}
-- select * from {{ ref('stg_fhv_tripdata') }} limit 100