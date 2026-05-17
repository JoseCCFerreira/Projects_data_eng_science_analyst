with date_range as (
    select distinct date(timestamp) as date_day
    from {{ ref('stg_sensor_readings') }}
    where timestamp is not null
)
select
    date_day,
    cast(strftime(date_day, '%Y') as integer) as year,
    cast(strftime(date_day, '%m') as integer) as month,
    cast(strftime(date_day, '%d') as integer) as day,
    cast(strftime(date_day, '%w') as integer) as day_of_week,
    strftime(date_day, '%Y-%m') as year_month
from date_range
order by date_day
