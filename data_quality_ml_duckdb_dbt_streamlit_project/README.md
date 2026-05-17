# data_quality_ml_duckdb_dbt_streamlit_project

Este projeto ilustra um pipeline completo de dados para sensores industriais, incluindo ingestão de dados, armazenamento transacional, camada analítica com DuckDB, transformações dbt, análise de qualidade, limpeza, resampling, filtragem de ruído, clustering, modelos preditivos e dashboard Streamlit.

## Estrutura do projeto

- `config/` - configurações YAML para caminhos e parâmetros.
- `data/raw/` - dados brutos gerados.
- `data/transactional/` - base de dados SQLite transacional.
- `data/analytical/` - base de dados DuckDB analítica.
- `data/processed/` - dados limpos, resampled e filtrados.
- `data/exports/` - resultados de clustering e previsões.
- `src/` - scripts Python para ingestão, armazenamento, transformação, qualidade e ML.
- `dbt_project/` - modelos e testes dbt para DuckDB.
- `streamlit_app/` - dashboard interativo com Plotly.
- `models/` - modelos treinados salvos.
- `reports/` - relatórios de qualidade e resultados.
- `docs/` - documentação do projeto e página pessoal.

## Como instalar

1. Crie e ative um ambiente virtual Python.
2. Instale dependências:

```bash
pip install -r requirements.txt
```

## Como usar

```bash
cd data_quality_ml_duckdb_dbt_streamlit_project
make setup
make generate-data
make load-sqlite
make load-duckdb
make dbt-run
make dbt-test
make quality-report
make clean-data
make resample
make filter-noise
make train-clustering
make train-prediction
make streamlit
```

## GitHub Pages

1. Crie um repositório no GitHub.
2. Adicione remote:

```bash
git remote add origin <URL>
```

3. Push:

```bash
git push -u origin main
```

4. Em Settings > Pages, escolha `main` e `/docs`.

## O que cada etapa faz

- `generate-data`: gera dados sintéticos e salva `data/raw/sensor_readings.csv`.
- `load-sqlite`: cria a base transacional SQLite com tabelas normalizadas.
- `load-duckdb`: cria a base analítica DuckDB carregando dados da SQLite.
- `dbt-run`: executa transformações dbt na base DuckDB.
- `dbt-test`: executa testes de qualidade dbt.
- `quality-report`: analisa qualidade dos dados e salva relatório.
- `clean-data`: aplica limpeza e gera dados processados.
- `resample`: executa resampling horário e diário.
- `filter-noise`: filtra ruídos e salva dataset filtrado.
- `train-clustering`: treina modelos de clustering e salva resultados.
- `train-prediction`: treina modelos preditivos e salva previsões.
- `streamlit`: abre o dashboard interativo.

## Escalabilidade

Este projeto foi construído de forma modular com separação clara entre ingestão, armazenamento, qualidade, transformação, ML e visualização. Para crescer, você pode introduzir PostgreSQL, Redshift, Airflow, Docker, CI/CD e monitorização de modelos.

## GitHub publishing steps

1. Criar repositório no GitHub.
2. Ligar remote local.
3. `git add .`
4. `git commit -m "Initial project structure for data quality ML pipeline"`
5. `git push -u origin main`.
6. Ativar GitHub Pages em `Settings > Pages`.
7. Configurar a pasta `/docs` como fonte.

## Licença

Projeto didático para aprendizagem e portfólio.
