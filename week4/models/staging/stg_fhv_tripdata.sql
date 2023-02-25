{{ config(materialized='view') }}


with tripdata as 
-- (
--   select *,
--     row_number() over(partition by vendorid, lpep_pickup_datetime) as rn
--   from {{ source('staging','fhv_tripdata') }}
--   where vendorid is not null 
-- )
(
  select * from {{ source('staging','fhv_tripdata') }}
  where date(pickup_datetime) between date('2019-01-01') and date('2019-12-31')
)

select cast(dispatching_base_num as string) as dispatching_base_num,
cast(pickup_datetime as timestamp) as pickup_datetime,
cast(dropoff_datetime as timestamp) as dropoff_datetime,
cast(pulocationid as integer) as pulocationid,
cast(dolocationid as integer) as dolocationid,
cast(sr_flag as string) as SR_Flag,
cast(Affiliated_base_number as string) as Affiliated_base_number,
from tripdata

{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
