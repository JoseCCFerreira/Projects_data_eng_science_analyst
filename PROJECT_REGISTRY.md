# Project Registry

Este repositorio central organiza os projetos locais que vivem dentro de `projects/`.

## Projetos

| Projeto | Foco | Stack principal | Estado |
| --- | --- | --- | --- |
| `global_fuel_shocks_intelligence_repo` | Choques globais de combustiveis, eventos e forecasting | Python, DuckDB, dbt, Streamlit, ML | Validado com testes e pipeline checks |
| `citibike_ebike_performance_repo` | Performance de e-bikes Citibike | Python, SQL, Streamlit, analytics | Projeto aplicado |
| `portugal_bike_geospatial_ml_repo` | Mobilidade e geospatial ML em Portugal | Python, SQL, ML, mapas | Projeto aplicado |
| `retail_analytics_learning_repo` | Retail analytics end-to-end | SQLite, DuckDB, dbt, Streamlit, ML | Projeto de aprendizagem |
| `retail_case_repo_with_dynamic_beginner_html` | Retail case com guias HTML | SQLite, DuckDB, HTML docs, ML | Projeto de aprendizagem |
| `tyrewear_intelligence_landing` | Inteligencia de desgaste de pneus | DuckDB, dbt, Streamlit, ML, docs | Projeto aplicado |

## Contrato da casa-mae

1. A raiz `Projecto/` e o repositorio central explicam o sistema inteiro.
2. Cada subprojeto mantem o seu proprio Git dentro de `projects/<nome>`.
3. A dashboard central le documentacao, dados e bases de dados sem reescrever os subprojetos.
4. As alteracoes globais ficam registadas em `CHANGELOG.md`.
5. As alteracoes de cada projeto ficam no changelog do respetivo projeto, quando existir.

## Servicos Integrados

| Projeto | Porta | App | Pipeline |
| --- | ---: | --- | --- |
| `global_fuel_shocks_intelligence_repo` | 8610 | `app.py` | `scripts/run_pipeline.py` |
| `citibike_ebike_performance_repo` | 8611 | `streamlit/app.py` | `python/run_pipeline.py` |
| `portugal_bike_geospatial_ml_repo` | 8612 | `streamlit/app.py` | `python/run_pipeline.py` |
| `retail_analytics_learning_repo` | 8613 | `streamlit/app.py` | `python/run_pipeline.py` |
| `retail_case_repo_with_dynamic_beginner_html` | 8614 | `streamlit/app.py` | `python/run_pipeline.py` |
| `tyrewear_intelligence_landing` | 8615 | `app.py` | n/a |
