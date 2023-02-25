{{ config(materialized='view') }}

select count(*) as number_of_records from {{ ref('stg_fhv_tripdata') }}
