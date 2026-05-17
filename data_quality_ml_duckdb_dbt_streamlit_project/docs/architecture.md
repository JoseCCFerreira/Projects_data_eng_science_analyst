# Architecture & Data Flow

## System Overview

Flowchart completo do projeto:

```
RAW DATA (CSV) → SQLite (OLTP) → DuckDB (OLAP) → dbt (Staging/Intermediate/Marts)
→ Data Quality → Cleaning → Resampling → Filtering → ML (Clustering + Prediction) → Streamlit
```

## Componentes Principais

### 1. **Geração de Dados** (src/ingest/)
- Dados sintéticos de sensores industriais
- 12 sensores, 4 máquinas, 4 localizações
- 4 meses de dados contínuos (jan-abr 2024)
- Problemas intencionais: 4% valores nulos, 2% outliers, 1% duplicados, 8% timestamps irregulares

### 2. **Camada Transacional** (SQLite - OLTP)
- Normalização completa com chaves estrangeiras
- Tabelas: sensors, machines, locations, machine_status, sensor_readings
- Simula operações de escrita e leitura transacionais
- Garantia de integridade referencial

### 3. **Camada Analítica** (DuckDB - OLAP)
- Cópia de dados para análise rápida
- Otimizado para consultas grandes
- Integração com dbt para transformações

### 4. **Transformações dbt**
- **Staging**: preparação de dados brutos, limpeza inicial
- **Intermediate**: validação de ranges físicos, lógica de negócio
- **Marts**: fact_sensor_measurements, dim_sensor, dim_date para análises

### 5. **Qualidade & Limpeza**
- Análise de valores nulos, duplicados, outliers
- Estatísticas descritivas (média, mediana, desvio padrão, skewness, kurtosis)
- Validação de ranges físicos
- Relatório executivo

### 6. **Preprocessing**
- Resampling: horário (mean/min/max/std) e diário
- Filtragem: rolling average, z-score, Savitzky-Golay

### 7. **Machine Learning**
- **Clustering**: K-Means, DBSCAN, Agglomerative, PCA 2D
- **Predição**: Linear Regression vs Random Forest para target_failure_risk

### 8. **Visualização** (Streamlit)
- 5 páginas: Overview, Quality, Analysis, Clustering, Predictions
