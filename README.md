# Projecto Central

Repositorio central dos projetos de dados, analytics, machine learning, documentacao, bases de dados e resultados.

## Estrutura

```text
Projecto/
  projects/             # Repositórios Git ativos
  learning_materials/   # PDFs, scripts e materiais de apoio soltos
  docs_html/            # Documentacao HTML central
  project_manager_app.py # Dashboard Streamlit central
  requirements-manager.txt
  PROJECT_REGISTRY.md   # Inventario dos projetos
  README.md             # Este índice
  CHANGELOG.md          # Registo de alterações da pasta principal
```

## Dashboard Central

```bash
python3 -m venv .venv-manager
source .venv-manager/bin/activate
pip install -r requirements-manager.txt
streamlit run project_manager_app.py --server.port 8600
```

A dashboard permite consultar projetos, documentação, ficheiros de dados, bases DuckDB/SQLite, gráficos rápidos, estado Git, resultados e uma academia explicativa da stack.

## Documentacao HTML Central

Abre diretamente no browser:

- `docs_html/index.html`
- `docs_html/concepts.html`
- `docs_html/projects.html`
- `docs_html/results.html`
- `docs_html/roadmap.html`

Estas paginas reorganizam a documentacao global para explicar Git, dbt, SQLite relacional, DuckDB, statistical analysis, machine learning, Streamlit, resultados e projetos.

## Repositórios

- `projects/global_fuel_shocks_intelligence_repo` - Global Fuel Shocks Intelligence.
- `projects/citibike_ebike_performance_repo` - Análise de performance e-bike Citibike.
- `projects/portugal_bike_geospatial_ml_repo` - Geospatial ML para bicicletas em Portugal.
- `projects/retail_analytics_learning_repo` - Retail analytics learning project.
- `projects/retail_case_repo_with_dynamic_beginner_html` - Retail case com guias HTML.
- `projects/tyrewear_intelligence_landing` - Tyre wear intelligence landing/app.

## Convenção

- Novos repositórios devem entrar em `projects/`.
- Materiais de estudo ou ficheiros avulsos ficam em `learning_materials/`.
- Alterações estruturais nesta pasta devem ser registadas em `CHANGELOG.md`.
- Cada projeto em `projects/` mantem o seu proprio repositorio Git; o repositorio central versiona a orquestracao, documentacao e servico.
