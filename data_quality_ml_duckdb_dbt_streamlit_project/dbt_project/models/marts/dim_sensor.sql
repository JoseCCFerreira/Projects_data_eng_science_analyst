select
    sensor_id,
    sensor_id as sensor_key,
    concat('Sensor ', sensor_id) as sensor_name,
    'industrial' as sensor_type
from (
    select distinct sensor_id
    from {{ ref('stg_sensor_readings') }}
)
