# Data Flow

O fluxo de dados cobre toda a cadeia de valor:

1. **Input**: geração de dados temporais de sensores em `data/raw`.
2. **Transacional**: normalização em SQLite com entidades de sensores, máquinas, locais e estados.
3. **Analítico**: ingestão em DuckDB para explorar e transformar dados sem alterar o raw.
4. **Transformação**: dbt organiza limpeza, validação e construção de marts.
5. **Qualidade**: análise estatística de nulos, duplicados, outliers e inconsistências.
6. **Machine Learning**: clustering para segmentação e regressão para previsão de risco.
7. **Visualização**: dashboard Streamlit com análises e resultados.
