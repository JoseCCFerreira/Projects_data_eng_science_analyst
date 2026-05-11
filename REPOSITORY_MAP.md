# Repository Map

This central repository is the operational wrapper around all local project repositories.

## Central Hub

- Local path: `/Users/carlosferreira/Projecto`
- Dashboard: `http://localhost:8600`
- Main app: `project_manager_app.py`
- Manifest: `central_project_manifest.json`

## Project Repositories

| Project | Repository | Local Path | Dashboard |
| --- | --- | --- | --- |
| Global Fuel Shocks Intelligence | <https://github.com/JoseCCFerreira/global-fuel-shocks-intelligence.git> | `projects/global_fuel_shocks_intelligence_repo` | `http://localhost:8610` |
| Citibike E-Bike Performance | <https://github.com/JoseCCFerreira/citibike-ebike-performance-repo.git> | `projects/citibike_ebike_performance_repo` | `http://localhost:8611` |
| Portugal Bike Geospatial ML | local repository | `projects/portugal_bike_geospatial_ml_repo` | `http://localhost:8612` |
| Retail Analytics Learning | <https://github.com/JoseCCFerreira/retail-analytics-learning-repo.git> | `projects/retail_analytics_learning_repo` | `http://localhost:8613` |
| Retail Case With Dynamic Beginner HTML | local repository | `projects/retail_case_repo_with_dynamic_beginner_html` | `http://localhost:8614` |
| Tyre Wear Intelligence | <https://github.com/JoseCCFerreira/tyrewear-intelligence.git> | `projects/tyrewear_intelligence_landing` | `http://localhost:8615` |

## Why The Central Repository Does Not Copy Project Contents

Each project already has its own Git repository. The central hub keeps the projects physically inside `projects/`, but version-controls the access layer, registry, documentation and service scripts. This avoids mixing histories and keeps each project independently runnable.

Use `central_project_manifest.json` as the machine-readable source of truth for the full local portfolio.
