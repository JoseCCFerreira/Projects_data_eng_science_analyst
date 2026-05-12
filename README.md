# Projects_data_eng_science_analyst

Central portfolio repository for **Data Engineering**, **Data Science**, **Analytics Engineering**, **Machine Learning**, **SQL databases**, **dbt**, **Streamlit dashboards** and documented analytical case studies.

Repositório central de portfólio para **Engenharia de Dados**, **Ciência de Dados**, **Analytics Engineering**, **Machine Learning**, **bases SQL**, **dbt**, **dashboards Streamlit** e projetos analíticos documentados.

![Central hub architecture](docs_html/assets/central_hub_architecture_bilingual.svg)

## What This Repository Is

This repository is the central access layer for a full local project portfolio. It does not flatten every project into one codebase. Instead, it keeps each project as an independent repository inside `projects/`, while this central repository provides:

- one Streamlit access panel
- one visual documentation hub
- one project registry
- one service manifest
- scripts to start and test every dashboard
- bilingual visual explanations
- links to every local dashboard and GitHub repository where available

Este repositório é a camada central de acesso para o portfólio local. Cada projeto continua independente dentro de `projects/`, mas este repositório central oferece:

- um painel Streamlit central
- documentação visual
- registo dos projetos
- manifesto de serviços
- scripts para arrancar e testar todos os dashboards
- explicações visuais em inglês e português
- links para dashboards e repositórios GitHub quando disponíveis

## Portfolio Overview

![Project portfolio](docs_html/assets/project_portfolio_bilingual.svg)

| Project | Repository | Dashboard | Main Purpose |
| --- | --- | --- | --- |
| Global Fuel Shocks Intelligence | <https://github.com/JoseCCFerreira/global-fuel-shocks-intelligence.git> | <http://localhost:8610> | Fuel prices, volatility, shocks, events, forecasting and ML |
| Citibike E-Bike Performance | <https://github.com/JoseCCFerreira/citibike-ebike-performance-repo.git> | <http://localhost:8611> | Urban mobility and e-bike performance analytics |
| Portugal Bike Geospatial ML | Local repository | <http://localhost:8612> | Geospatial mobility analysis and machine learning |
| Retail Analytics Learning | <https://github.com/JoseCCFerreira/retail-analytics-learning-repo.git> | <http://localhost:8613> | End-to-end retail analytics learning path |
| Retail Case With Dynamic Beginner HTML | Local repository | <http://localhost:8614> | Beginner-friendly retail case with SQL, HTML docs and ML |
| Tyre Wear Intelligence | <https://github.com/JoseCCFerreira/tyrewear-intelligence.git> | <http://localhost:8615> | Tyre wear, statistics, clustering, ML and recommendations |

## Repository Structure

```text
Projects_data_eng_science_analyst/
  project_manager_app.py           # Central Streamlit access panel
  central_project_manifest.json    # Machine-readable portfolio map
  PROJECT_REGISTRY.md              # Human-readable project registry
  REPOSITORY_MAP.md                # Repository links, paths and dashboards
  requirements-manager.txt         # Central manager dependencies
  scripts/
    start_all_dashboards.py        # Starts every project dashboard
    check_services.py              # Tests every dashboard endpoint
  docs_html/
    index.html                     # Main HTML documentation page
    visuals.html                   # English visual guide
    visuals_pt.html                # Portuguese visual guide
    assets/                        # Versioned SVG diagrams
  docs/
    en/VISUAL_GUIDE.md             # English Markdown visual guide
    pt/GUIA_VISUAL.md              # Portuguese Markdown visual guide
  projects/
    <individual project repos>     # Independent Git repositories
```

## How To Run Everything

Create or activate the central manager environment:

```bash
python3 -m venv .venv-manager
source .venv-manager/bin/activate
pip install -r requirements-manager.txt
```

Start the central access panel:

```bash
streamlit run project_manager_app.py --server.port 8600
```

Start every project dashboard:

```bash
python scripts/start_all_dashboards.py
```

Check that everything is running:

```bash
python scripts/check_services.py
```

Expected result:

```text
200 Central Project Hub http://localhost:8600
200 Global Fuel Shocks Intelligence http://localhost:8610
200 Citibike E-Bike Performance http://localhost:8611
200 Portugal Bike Geospatial ML http://localhost:8612
200 Retail Analytics Learning http://localhost:8613
200 Retail Case With Dynamic Beginner HTML http://localhost:8614
200 Tyre Wear Intelligence http://localhost:8615
```

## Dashboard Access

![Dashboard access](docs_html/assets/dashboard_access_bilingual.svg)

The central dashboard at <http://localhost:8600> includes:

- project access panel
- dashboard launch buttons
- repository links
- Git status
- documentation browser
- data file browser
- DuckDB and SQLite table preview
- chart generator
- mathematical and statistical theory
- machine-learning explanations
- service logs
- pipeline controls

## Data Engineering Flow

![Data pipeline](docs_html/assets/data_pipeline_bilingual.svg)

The projects follow the same general analytical flow:

1. **Sources**: APIs, CSV, Excel files, generated data or public datasets.
2. **Raw data**: original extracts are stored as reproducible inputs.
3. **Processing**: Python scripts clean, normalize and enrich the data.
4. **Databases**: SQLite is used for relational/OLTP examples; DuckDB is used for analytical/OLAP work.
5. **Transformations**: SQL and dbt-style models create staging, intermediate and mart layers.
6. **Analysis**: statistical summaries, correlations, event studies, forecasts and machine-learning models.
7. **Dashboards**: Streamlit apps expose results, charts, maps, tables and exports.

Fluxo em português:

1. **Fontes**: APIs, CSV, Excel, dados gerados ou datasets públicos.
2. **Dados brutos**: extrações originais guardadas como input reproduzível.
3. **Processamento**: scripts Python limpam, normalizam e enriquecem os dados.
4. **Bases de dados**: SQLite para exemplos relacionais/OLTP; DuckDB para análise/OLAP.
5. **Transformações**: SQL e dbt criam camadas staging, intermediate e marts.
6. **Análise**: estatística, correlações, eventos, forecasts e modelos ML.
7. **Dashboards**: Streamlit apresenta resultados, gráficos, mapas, tabelas e exports.

## Git Workflow

![Git workflow](docs_html/assets/git_workflow_bilingual.svg)

This central repository has its own Git history. Each project inside `projects/` also keeps its own Git history.

Recommended workflow:

```bash
git status --short
git diff
git add <files>
git commit -m "Clear message"
git log --oneline
```

This keeps the central hub clean while preserving each project as an independent deliverable.

## Mathematics, Statistics And Machine Learning

![Mathematics statistics and ML](docs_html/assets/math_ml_concepts_bilingual.svg)

The portfolio demonstrates practical use of:

- mean, variance and standard deviation
- z-scores and outlier detection
- correlation matrices
- time-series returns and rolling volatility
- regression baselines
- classification metrics such as accuracy, precision and recall
- clustering and distance-based segmentation
- Random Forest models and feature importance
- forecast baselines and model limitations

Português:

- média, variância e desvio padrão
- z-scores e deteção de outliers
- matrizes de correlação
- retornos temporais e volatilidade móvel
- regressão como baseline
- métricas de classificação como accuracy, precision e recall
- clustering e segmentação por distância
- Random Forest e importância de features
- forecasts e limitações dos modelos

## Project Details

### Global Fuel Shocks Intelligence

Context: global fuel-price variation, shocks, wars, disasters, population and macro context.

Code: Python pipeline, DuckDB database, dbt-style transformations, Streamlit app.

Results: statistical summaries, event-study outputs, forecast baseline, feature importance and model metrics.

ML: Random Forest classifier for price-jump risk and Random Forest regressor for monthly-change modeling.

### Citibike E-Bike Performance

Context: bike-sharing and e-bike performance analytics.

Code: Python pipeline, SQL analysis and Streamlit dashboard.

Results: usage patterns, operational metrics and visual analytics.

ML: prepared structure for performance and demand pattern experiments.

### Portugal Bike Geospatial ML

Context: mobility and geospatial analytics in Portugal.

Code: Python scripts, geospatial features, visual documentation and Streamlit.

Results: maps, technical explanations, practical ML theory and geographic analysis.

ML: geospatial feature engineering for prioritization, segmentation or prediction.

### Retail Analytics Learning

Context: full learning path from relational databases to dashboards and ML.

Code: SQLite, DuckDB, dbt, Python scripts, Streamlit and optional deep-learning material.

Results: retail KPIs, relational models, analytical marts, visualizations and model outputs.

ML: retail feature engineering, predictive modeling and evaluation.

### Retail Case With Dynamic Beginner HTML

Context: guided beginner-friendly retail analytics case.

Code: CSV data, SQLite/DuckDB databases, Python scripts, Streamlit and HTML documentation.

Results: beginner guides, SQL outputs, dashboards and model-ready tables.

ML: practical retail decision-support modeling.

### Tyre Wear Intelligence

Context: tyre wear, tread depth, vehicle context and recommendation analytics.

Code: multi-page Streamlit app, Python, DuckDB/dbt concepts and technical documentation.

Results: statistical tests, clustering pages, ML pages, recommendation views and export-oriented decision center.

ML: clustering, supervised learning, deep-learning pages and tyre recommendation logic.

## Documentation Links

- LinkedIn presentation pack: [linkedin/](linkedin/)
- English visual guide: [docs/en/VISUAL_GUIDE.md](docs/en/VISUAL_GUIDE.md)
- Portuguese visual guide: [docs/pt/GUIA_VISUAL.md](docs/pt/GUIA_VISUAL.md)
- English stack quick reference: [docs/en/STACK_QUICK_REFERENCE.md](docs/en/STACK_QUICK_REFERENCE.md)
- Portuguese stack quick reference: [docs/pt/REFERENCIA_RAPIDA_STACK.md](docs/pt/REFERENCIA_RAPIDA_STACK.md)
- HTML home: [docs_html/index.html](docs_html/index.html)
- HTML quick reference: [docs_html/stack_reference.html](docs_html/stack_reference.html)
- HTML Portuguese quick reference: [docs_html/stack_reference_pt.html](docs_html/stack_reference_pt.html)
- HTML visual guide: [docs_html/visuals.html](docs_html/visuals.html)
- HTML Portuguese visual guide: [docs_html/visuals_pt.html](docs_html/visuals_pt.html)
- Services page: [docs_html/services.html](docs_html/services.html)
- Theory page: [docs_html/theory.html](docs_html/theory.html)
- Results page: [docs_html/results.html](docs_html/results.html)

## Repository Policy

- This central repository versions the hub, documentation, diagrams, registry, manifest and service scripts.
- Individual project code stays in its own repository under `projects/`.
- `.venv-manager` environments and logs are not committed.
- The central dashboard can start, stop and inspect project services without merging their histories.

## Current Repository Name

**Projects_data_eng_science_analyst**

This is the intended repository name for publishing the central hub.
