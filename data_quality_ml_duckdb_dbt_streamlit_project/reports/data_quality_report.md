# Data Quality Report


## Resumo Executivo
- Registos totais: 32130
- Variáveis: 11
- Duplicados detectados: 268
- Valores nulos totais: 5285


## Problemas principais
- Valores nulos e timestamps ausentes podem afetar análises temporais e modelagem.
- Duplicados podem inflar contagens e distorcer médias.
- Outliers em temperatura, pressão e energia podem indicar medições anômalas ou falhas de sensor.
- Categorias inconsistentes em `machine_status` e `location` devem ser normalizadas.


## Estatísticas descritivas
| feature             |   count |       mean |   median |       std |      min |     max |      skew |   kurtosis |
|:--------------------|--------:|-----------:|---------:|----------:|---------:|--------:|----------:|-----------:|
| temperature         |   30849 |  74.0077   |  74.97   | 21.4277   | -129.036 | 190.998 | -4.14346  |  33.9465   |
| humidity            |   30849 |  43.8965   |  43.24   | 10.3743   |    7.46  | 140.9   |  1.6929   |   8.27625  |
| pressure            |   30849 | 101.217    | 101.3    |  3.65899  |   69.01  | 123.45  | -3.49661  |  49.3947   |
| vibration           |   30849 |   1.21406  |   1.204  |  0.576883 |    0     |   3.752 |  0.197982 |  -0.271552 |
| energy_consumption  |   32130 | 148.053    | 143.02   | 48.9242   |   47.37  | 641.19  |  4.53014  |  29.0718   |
| target_failure_risk |   32130 |   0.317047 |   0.2991 |  0.245994 |    0     |   1     |  0.374986 |  -0.80592  |


## Valores nulos por coluna
| feature             |   missing_count |   missing_ratio |
|:--------------------|----------------:|----------------:|
| timestamp           |             161 |      0.00501089 |
| sensor_id           |               0 |      0          |
| machine_id          |               0 |      0          |
| location            |               0 |      0          |
| temperature         |            1281 |      0.0398693  |
| humidity            |            1281 |      0.0398693  |
| pressure            |            1281 |      0.0398693  |
| vibration           |            1281 |      0.0398693  |
| energy_consumption  |               0 |      0          |
| machine_status      |               0 |      0          |
| target_failure_risk |               0 |      0          |


## Outliers detectados (IQR)
| feature             |   outliers |   outlier_ratio |   lower_bound |   upper_bound |
|:--------------------|-----------:|----------------:|--------------:|--------------:|
| temperature         |        549 |      0.0170868  |      34.075   |     116.035   |
| humidity            |        700 |      0.0217865  |      20.34    |      66.34    |
| pressure            |        799 |      0.0248677  |      99.1     |     103.5     |
| vibration           |        120 |      0.00373483 |      -0.4045  |       2.8075  |
| energy_consumption  |        705 |      0.0219421  |      67.6838  |     218.634   |
| target_failure_risk |          0 |      0          |      -0.52395 |       1.12205 |


## Correlações principais
|                     |   temperature |    humidity |    pressure |   vibration |   energy_consumption |   target_failure_risk |
|:--------------------|--------------:|------------:|------------:|------------:|---------------------:|----------------------:|
| temperature         |    1          | -0.178267   |  0.0548757  | -0.00257058 |          -0.0864725  |            0.504358   |
| humidity            |   -0.178267   |  1          | -0.0936466  | -0.00719475 |           0.469697   |            0.00410835 |
| pressure            |    0.0548757  | -0.0936466  |  1          |  0.00142146 |          -0.109994   |            0.00215367 |
| vibration           |   -0.00257058 | -0.00719475 |  0.00142146 |  1          |          -0.00446797 |           -0.00556736 |
| energy_consumption  |   -0.0864725  |  0.469697   | -0.109994   | -0.00446797 |           1          |            0.291681   |
| target_failure_risk |    0.504358   |  0.00410835 |  0.00215367 | -0.00556736 |           0.291681   |            1          |


## Exemplo de linhas problemáticas
- `timestamp` ausente em algumas linhas;
- `sensor_999` aparece como sensor inválido;
- valores de pressão com +20 ou -30 hPa são fisicamente impossíveis;
- `machine_status` em maiúsculas ou espaços extras são inconsistentes.


## Recomendações
- Limpar duplicados e imputar ou remover registros com timestamps nulos;
- Normalizar categorias antes da modelagem;
- Isolar outliers por equipamento antes de calcular métricas de desempenho;
- Revisar faixas físicas e validar sensores com manutenção preventiva;
- Usar dbt tests para rastrear qualidade de dados após transformações.