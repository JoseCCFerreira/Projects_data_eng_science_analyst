select
    reading_id,
    timestamp,
    sensor_id,
    machine_id,
    location,
    temperature,
    humidity,
    pressure,
    vibration,
    energy_consumption,
    machine_status,
    target_failure_risk
from {{ ref('int_clean_sensor_readings') }}
