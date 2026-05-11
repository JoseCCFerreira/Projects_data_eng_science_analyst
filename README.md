# Central Project Hub

Central repository for the local data, analytics, machine learning, documentation, database and dashboard portfolio.

This repository is the access layer. The individual project repositories remain inside `projects/` and keep their own Git history.

## Structure

```text
Projecto/
  projects/              # Individual Git repositories
  learning_materials/    # Loose PDFs, scripts and study materials
  docs_html/             # Central English HTML documentation
  project_manager_app.py # Central Streamlit access panel
  central_project_manifest.json
  REPOSITORY_MAP.md
  scripts/               # Operational scripts for all dashboards
  requirements-manager.txt
  PROJECT_REGISTRY.md    # Project inventory and service map
  README.md
  CHANGELOG.md
```

## Run The Central Access Panel

```bash
python3 -m venv .venv-manager
source .venv-manager/bin/activate
pip install -r requirements-manager.txt
streamlit run project_manager_app.py --server.port 8600
```

Open:

```text
http://localhost:8600
```

The central panel gives access to:

- all project folders and dashboards
- Git status and latest commit
- documentation and HTML guides
- CSV, Excel, Parquet and JSON data files
- DuckDB and SQLite databases
- quick charts from tabular data
- project service start/stop controls
- pipeline execution logs
- mathematical, statistical, programming and machine-learning explanations

## Start And Test Everything

Start every project dashboard from the central repository:

```bash
source .venv-manager/bin/activate
python scripts/start_all_dashboards.py
```

Check that the central panel and all project dashboards respond:

```bash
python scripts/check_services.py
```

## Project Dashboard Links

| Project | Repository | Dashboard | App entrypoint | Pipeline |
| --- | --- | --- | --- | --- |
| `global_fuel_shocks_intelligence_repo` | <https://github.com/JoseCCFerreira/global-fuel-shocks-intelligence.git> | `http://localhost:8610` | `app.py` | `scripts/run_pipeline.py` |
| `citibike_ebike_performance_repo` | <https://github.com/JoseCCFerreira/citibike-ebike-performance-repo.git> | `http://localhost:8611` | `streamlit/app.py` | `python/run_pipeline.py` |
| `portugal_bike_geospatial_ml_repo` | local: `projects/portugal_bike_geospatial_ml_repo` | `http://localhost:8612` | `streamlit/app.py` | `python/run_pipeline.py` |
| `retail_analytics_learning_repo` | <https://github.com/JoseCCFerreira/retail-analytics-learning-repo.git> | `http://localhost:8613` | `streamlit/app.py` | `python/run_pipeline.py` |
| `retail_case_repo_with_dynamic_beginner_html` | local: `projects/retail_case_repo_with_dynamic_beginner_html` | `http://localhost:8614` | `streamlit/app.py` | `python/run_pipeline.py` |
| `tyrewear_intelligence_landing` | <https://github.com/JoseCCFerreira/tyrewear-intelligence.git> | `http://localhost:8615` | `app.py` | n/a |

Use the `Services` view in the central panel to install dependencies, start dashboards, stop dashboards and run pipelines.

## Central HTML Documentation

Open these files directly in a browser or through the `Central HTML` view:

- `docs_html/index.html`
- `docs_html/concepts.html`
- `docs_html/theory.html`
- `docs_html/services.html`
- `docs_html/projects.html`
- `docs_html/results.html`
- `docs_html/roadmap.html`

The documentation explains the full journey: creation context, Git, relational SQLite, DuckDB, dbt, programming, code structure, mathematical/statistical theory, machine learning, Streamlit dashboards, results and interpretation.

## Repository Policy

- New projects belong in `projects/`.
- Loose study files belong in `learning_materials/`.
- The central repository versions orchestration, documentation and the access service.
- Each project inside `projects/` keeps its own Git repository and history.
- Structural changes in the central hub must be recorded in `CHANGELOG.md`.
