# Project Registry

This central repository organizes the local projects inside `projects/`.

## Projects

| Project | Purpose | Repository | Dashboard |
| --- | --- | --- | --- |
| `global_fuel_shocks_intelligence_repo` | Global fuel shocks, events, volatility, forecasting and geo context | <https://github.com/JoseCCFerreira/global-fuel-shocks-intelligence.git> | `http://localhost:8610` |
| `citibike_ebike_performance_repo` | E-bike and urban mobility performance analytics | <https://github.com/JoseCCFerreira/citibike-ebike-performance-repo.git> | `http://localhost:8611` |
| `portugal_bike_geospatial_ml_repo` | Bike and mobility geospatial machine learning for Portugal | local only | `http://localhost:8612` |
| `retail_analytics_learning_repo` | End-to-end retail analytics learning path | <https://github.com/JoseCCFerreira/retail-analytics-learning-repo.git> | `http://localhost:8613` |
| `retail_case_repo_with_dynamic_beginner_html` | Guided retail case with beginner-friendly HTML documentation | local only | `http://localhost:8614` |
| `tyrewear_intelligence_landing` | Tyre wear intelligence, statistics, ML and decision support | <https://github.com/JoseCCFerreira/tyrewear-intelligence.git> | `http://localhost:8615` |

## Central Hub Contract

1. The root `Projecto/` repository explains and operates the whole system.
2. Every subproject keeps its own Git repository inside `projects/<name>`.
3. The central dashboard reads documentation, data and databases without rewriting project internals.
4. Global changes are recorded in `CHANGELOG.md`.
5. Project-specific changes stay in the relevant project changelog when available.

## Integrated Services

| Project | Port | App | Pipeline |
| --- | ---: | --- | --- |
| `global_fuel_shocks_intelligence_repo` | 8610 | `app.py` | `scripts/run_pipeline.py` |
| `citibike_ebike_performance_repo` | 8611 | `streamlit/app.py` | `python/run_pipeline.py` |
| `portugal_bike_geospatial_ml_repo` | 8612 | `streamlit/app.py` | `python/run_pipeline.py` |
| `retail_analytics_learning_repo` | 8613 | `streamlit/app.py` | `python/run_pipeline.py` |
| `retail_case_repo_with_dynamic_beginner_html` | 8614 | `streamlit/app.py` | `python/run_pipeline.py` |
| `tyrewear_intelligence_landing` | 8615 | `app.py` | n/a |

## Explanation Coverage

The central hub documents each project through these lenses:

- creation purpose and analytical context
- data sources and database layer
- programming structure and code entrypoints
- mathematical and statistical concepts
- machine-learning workflow and interpretation
- dashboards, charts, results and limitations
