with sensor_readings as (
    select * from {{ source('main', 'sensor_readings') }}
),

sensors as (
    select * from {{ source('main', 'sensors') }}
),

machines as (
    select * from {{ source('main', 'machines') }}
),

locations as (
    select * from {{ source('main', 'locations') }}
),

machine_status as (
    select * from {{ source('main', 'machine_status') }}
)

select
    sr.reading_id,
    sr.timestamp,
    s.sensor_name as sensor_id,
    m.machine_name as machine_id,
    l.location_name as location,
    sr.temperature,
    sr.humidity,
    sr.pressure,
    sr.vibration,
    sr.energy_consumption,
    case
        when lower(trim(ms.machine_status)) = 'running' then 'running'
        when lower(trim(ms.machine_status)) = 'idle' then 'idle'
        when lower(trim(ms.machine_status)) = 'maintenance' then 'maintenance'
        when lower(trim(ms.machine_status)) = 'fault' then 'fault'
        else 'Unknown'
    end as machine_status,
    sr.target_failure_risk
from sensor_readings sr
left join sensors s on sr.sensor_id = s.sensor_id
left join machines m on sr.machine_id = m.machine_id
left join locations l on sr.location_id = l.location_id
left join machine_status ms on sr.status_id = ms.status_id
