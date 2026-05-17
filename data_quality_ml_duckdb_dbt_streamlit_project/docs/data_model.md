# Data Model

## Modelo Transacional

A camada transacional utiliza normalização para reduzir redundância e suportar operações OLTP.

- `locations`: guarda locais de instalação.
- `machines`: guarda as máquinas monitoradas.
- `sensors`: guarda os sensores e seus tipos.
- `machine_status`: guarda estados possíveis das máquinas.
- `sensor_readings`: guarda as leituras com chaves estrangeiras.

## Modelo Analítico

A camada analítica agrupa dados em tabelas prontas para análise:

- `fact_sensor_measurements`: tabela de fatos com métricas e risco.
- `dim_sensor`: dimensão de sensores.
- `dim_date`: dimensão de datas para análises temporais.

## Diferença entre Relacional e Analítico

- Relacional foca em transações, consistência e normalização.
- Analítico foca em consultas rápidas, agregações e relatórios.

## OLTP vs OLAP

- **OLTP**: operações de leitura/escrita frequentes, transações detalhadas.
- **OLAP**: consultas analíticas, agregações e modelos de negócio.
