with cleaned as (
    select
        reading_id,
        timestamp,
        sensor_id,
        machine_id,
        location,
        case
            when temperature < -20 or temperature > 120 then null
            else temperature
        end as temperature,
        case
            when humidity < 0 or humidity > 100 then null
            else humidity
        end as humidity,
        case
            when pressure < 80 or pressure > 120 then null
            else pressure
        end as pressure,
        case
            when vibration < 0 then null
            else vibration
        end as vibration,
        case
            when energy_consumption < 0 then null
            else energy_consumption
        end as energy_consumption,
        machine_status,
        target_failure_risk
    from {{ ref('stg_sensor_readings') }}
)

select *
from cleaned
