from __future__ import annotations

import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parent
PROJECTS_DIR = ROOT / "projects"
LEARNING_DIR = ROOT / "learning_materials"
DOCS_HTML_DIR = ROOT / "docs_html"

DOC_EXTENSIONS = {".md", ".html", ".htm", ".pdf", ".txt"}
DATA_EXTENSIONS = {".csv", ".xlsx", ".xls", ".parquet", ".json"}
DB_EXTENSIONS = {".duckdb", ".db", ".sqlite", ".sqlite3"}
IGNORED_DIRS = {".git", ".venv", ".venv-dbt", ".venv_mac", "__pycache__", ".pytest_cache", "target", "logs"}


ACADEMY_TOPICS = {
    "Git": {
        "purpose": "Version control for commits, history, recovery and collaboration.",
        "steps": [
            "Check the repository state before changing anything: git status --short.",
            "Read the changes carefully: git diff.",
            "Stage a small coherent unit of work: git add files.",
            "Save the work with context: git commit -m \"clear message\".",
            "Inspect history when explaining the project: git log --oneline.",
        ],
        "result": "A clean history where each commit explains one technical decision.",
    },
    "dbt": {
        "purpose": "Transform data with organized, testable and documented SQL.",
        "steps": [
            "Load raw sources into DuckDB or another analytical warehouse.",
            "Create staging models to clean names, types and grain.",
            "Create intermediate models for joins and business rules.",
            "Create marts that answer final analytical questions.",
            "Run dbt build to execute models and tests together.",
        ],
        "result": "An analytical layer with lineage, readable SQL and quality tests.",
    },
    "Relational SQLite": {
        "purpose": "Represent transactional operations through related tables.",
        "steps": [
            "Separate entities such as customers, products, stores and transactions.",
            "Define primary keys and foreign keys.",
            "Create indexes for frequent queries.",
            "Query with joins, where clauses, group by and window functions when appropriate.",
            "Use SQLite for teaching, compact apps and OLTP-style examples.",
        ],
        "result": "A compact database that teaches relational integrity and SQL querying.",
    },
    "DuckDB": {
        "purpose": "Run fast local analytics over CSV, Parquet and larger analytical tables.",
        "steps": [
            "Read files directly or materialize them as tables.",
            "Create analytical views by topic.",
            "Move heavy joins and aggregations into DuckDB.",
            "Serve data to Python, dbt and Streamlit.",
            "Store reproducible .duckdb snapshots when useful.",
        ],
        "result": "A local OLAP engine for exploring results without an external server.",
    },
    "Statistical Analysis": {
        "purpose": "Turn data into measured signals: distributions, variation, risk and relationships.",
        "steps": [
            "Check time coverage and missing values.",
            "Compute means, medians, standard deviations and quantiles.",
            "Analyze volatility, outliers and z-scores.",
            "Measure correlations and event-study windows.",
            "Document limits before suggesting causality.",
        ],
        "result": "More honest conclusions, with signal separated from noise.",
    },
    "Machine Learning": {
        "purpose": "Learn patterns for prediction, classification or ranking.",
        "steps": [
            "Define the target and features without information leakage.",
            "Split train/test data, respecting time order for time series.",
            "Train a baseline and the main model.",
            "Measure error, stability and feature importance.",
            "Explain when the model should and should not be used.",
        ],
        "result": "Models that are evaluated, not merely trained.",
    },
    "Streamlit": {
        "purpose": "Turn data and models into an interactive user experience.",
        "steps": [
            "Load data from CSV, SQLite or DuckDB.",
            "Create filters and selectors around the user's question.",
            "Show metrics, tables, charts and downloads.",
            "Separate pages by workflow.",
            "Use caching to keep the app responsive.",
        ],
        "result": "A practical interface for exploring a project without opening code.",
    },
    "Results": {
        "purpose": "Close the loop between data, charts, interpretation and decisions.",
        "steps": [
            "Generate reproducible outputs.",
            "Validate rows, columns and metrics.",
            "Create charts that answer clear questions.",
            "Write conclusions with methodology and limitations.",
            "Record changes in the changelog.",
        ],
        "result": "An end-to-end explainable result.",
    },
}

THEORY = {
    "en": {
        "title": "Mathematical and statistical theory",
        "intro": "This section connects formulas to the projects. The goal is to understand what each metric measures, when to use it and how to interpret it.",
        "topics": {
            "Mean, variance and standard deviation": {
                "formula": "mean = sum(x_i) / n; variance = sum((x_i - mean)^2) / (n - 1); std = sqrt(variance)",
                "example": "If monthly growth values are [2, -1, 4, 0], the mean is 1.25. Standard deviation measures how far months move away from that average.",
                "use": "Used in fuel volatility, average retail sales and bike usage distributions.",
            },
            "Z-score and outliers": {
                "formula": "z = (x - mean) / standard_deviation",
                "example": "A z-score of 2.8 means the value is 2.8 standard deviations above typical behavior.",
                "use": "In the fuel project, price_jump_flag marks shocks when monthly change has a high absolute z-score.",
            },
            "Correlation": {
                "formula": "corr(X,Y) = cov(X,Y) / (std(X) * std(Y))",
                "example": "If fuel price and conflict deaths move upward together, correlation may be positive. Correlation does not prove causality.",
                "use": "Correlation matrices in fuel, tyrewear, retail and citibike projects.",
            },
            "Linear regression": {
                "formula": "y = beta_0 + beta_1*x_1 + ... + error",
                "example": "Predict sales using price, discount and seasonality. beta_1 indicates how much y changes when x_1 increases by one unit.",
                "use": "Interpretable baseline before more complex models.",
            },
            "Classification and confusion matrix": {
                "formula": "accuracy = correct / total; precision = TP/(TP+FP); recall = TP/(TP+FN)",
                "example": "For a price-shock model, a false positive warns about a shock that did not happen; a false negative misses a real shock.",
                "use": "Risk, fraud, churn or price-jump models.",
            },
            "Time series": {
                "formula": "return_t = (value_t / value_{t-1} - 1) * 100",
                "example": "If price goes from 100 to 110, return is 10%. If it goes from 110 to 99, return is -10%.",
                "use": "Fuel forecasting, sales evolution, bike demand and wear over time.",
            },
            "Clustering": {
                "formula": "euclidean distance = sqrt(sum((x_i - y_i)^2))",
                "example": "Group similar stores by sales, margin and customer count.",
                "use": "Segmentation in retail, tyres, mobility and usage patterns.",
            },
        },
    },
}

PROJECT_CONTEXT = {
    "global_fuel_shocks_intelligence_repo": {
        "title": "Global Fuel Shocks Intelligence",
        "context": "A global commodity analytics project focused on fuel prices, volatility, shock detection, wars, disasters, population and macro context.",
        "creation": "Built as an end-to-end reproducible analytics case: public data ingestion, normalization, DuckDB storage, dbt-style marts, statistical outputs, forecasting and a Streamlit exploration layer.",
        "programming": "Python scripts orchestrate fetch, preparation, DuckDB setup, analysis and validation. The Streamlit app reads processed outputs and database marts.",
        "math": "Uses percentage returns, rolling volatility, z-scores, correlations, event summaries and baseline forecasting bands.",
        "ml": "Random Forest models estimate jump-risk classification and monthly-change regression, with metrics and feature importance exported.",
        "results": "Key outputs include statistical summaries, correlation matrices, event-study summaries, forecast baselines, model metrics and geo distributions.",
    },
    "citibike_ebike_performance_repo": {
        "title": "Citibike E-Bike Performance",
        "context": "Urban mobility analytics focused on e-bike usage, demand and performance patterns.",
        "creation": "Created as an applied data product around bike-sharing data, with pipeline, SQL, documentation and Streamlit exploration.",
        "programming": "Python pipeline code prepares datasets; SQL supports analytical questions; Streamlit exposes interactive exploration.",
        "math": "Uses time aggregation, utilization metrics, distributions, comparative analysis and trend visualization.",
        "ml": "Supports experiments around demand/performance patterns and feature-based modeling when prepared data is available.",
        "results": "Dashboards and HTML documentation explain usage patterns, experiment outputs and operational insights.",
    },
    "portugal_bike_geospatial_ml_repo": {
        "title": "Portugal Bike Geospatial ML",
        "context": "A geospatial machine-learning project for understanding bike/mobility patterns in Portugal.",
        "creation": "Built to connect geography, tabular analytics, model features and visual explanations.",
        "programming": "Python scripts prepare data and models; Streamlit and HTML pages make the geographic analysis accessible.",
        "math": "Uses spatial features, distance-style reasoning, statistical comparisons and model evaluation metrics.",
        "ml": "Geospatial features feed machine-learning workflows for segmentation, prediction or prioritization.",
        "results": "Outputs emphasize maps, practical ML theory, coding explanations and technical documentation.",
    },
    "retail_analytics_learning_repo": {
        "title": "Retail Analytics Learning",
        "context": "A teaching-oriented retail analytics project covering OLTP, OLAP, visualization, machine learning and governance.",
        "creation": "Created as a full learning path from relational modeling to analytical marts, dashboards and ML.",
        "programming": "SQLite demonstrates relational transactions; DuckDB supports analytics; Python scripts generate, process and model data.",
        "math": "Uses sales aggregation, margin metrics, distributions, correlations, forecasting ideas and classification/regression metrics.",
        "ml": "Includes retail ML examples such as demand signals, feature engineering, model metrics and optional deep-learning extensions.",
        "results": "The project produces databases, processed data, Streamlit views, dbt models and extensive beginner-friendly documentation.",
    },
    "retail_case_repo_with_dynamic_beginner_html": {
        "title": "Retail Case with Dynamic Beginner HTML",
        "context": "A retail case study packaged with beginner-friendly HTML documentation and practical datasets.",
        "creation": "Built to explain the same analytical journey in a highly guided format: raw tables, SQL, DuckDB, dashboards and ML.",
        "programming": "Python and SQL scripts create and analyze retail data; HTML pages document the steps in an approachable way.",
        "math": "Uses relational joins, sales KPIs, aggregation, distribution analysis and model evaluation concepts.",
        "ml": "Covers practical feature preparation and model outputs for retail decision support.",
        "results": "Includes CSV tables, SQLite/DuckDB databases, Streamlit apps and detailed HTML learning guides.",
    },
    "tyrewear_intelligence_landing": {
        "title": "Tyre Wear Intelligence",
        "context": "A decision-support analytics project for tyre wear, tread depth, vehicle context and recommendations.",
        "creation": "Built as a polished applied analytics product with data exploration, dbt/DuckDB concepts, statistical tests, ML and role-based documentation.",
        "programming": "Python and Streamlit power a multi-page analytical app; docs explain SQL, dbt, SQLite/DuckDB and modeling choices.",
        "math": "Uses tread-depth change, statistical tests, correlations, clustering, numerical reasoning and recommendation logic.",
        "ml": "Includes clustering, machine learning, deep-learning pages and feature-based tyre recommendations.",
        "results": "Results appear through a Streamlit decision center, documentation pages, snapshots and export-oriented views.",
    },
}

PROJECT_SERVICES = {
    "global_fuel_shocks_intelligence_repo": {
        "port": 8610,
        "app": "app.py",
        "pipeline": "scripts/run_pipeline.py",
        "requirements": "requirements.txt",
    },
    "citibike_ebike_performance_repo": {
        "port": 8611,
        "app": "streamlit/app.py",
        "pipeline": "python/run_pipeline.py",
        "requirements": "requirements.txt",
    },
    "portugal_bike_geospatial_ml_repo": {
        "port": 8612,
        "app": "streamlit/app.py",
        "pipeline": "python/run_pipeline.py",
        "requirements": "requirements.txt",
    },
    "retail_analytics_learning_repo": {
        "port": 8613,
        "app": "streamlit/app.py",
        "pipeline": "python/run_pipeline.py",
        "requirements": "requirements.txt",
    },
    "retail_case_repo_with_dynamic_beginner_html": {
        "port": 8614,
        "app": "streamlit/app.py",
        "pipeline": "python/run_pipeline.py",
        "requirements": "requirements.txt",
    },
    "tyrewear_intelligence_landing": {
        "port": 8615,
        "app": "app.py",
        "pipeline": None,
        "requirements": "requirements.txt",
    },
}


@dataclass(frozen=True)
class Project:
    name: str
    path: Path


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


@st.cache_data(show_spinner=False)
def list_projects() -> list[Project]:
    if not PROJECTS_DIR.exists():
        return []
    return [Project(path.name, path) for path in sorted(PROJECTS_DIR.iterdir()) if path.is_dir()]


def safe_walk_files(base: Path, extensions: set[str] | None = None) -> list[Path]:
    files: list[Path] = []
    for path in base.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file() and (extensions is None or path.suffix.lower() in extensions):
            files.append(path)
    return sorted(files)


@st.cache_data(show_spinner=False)
def project_inventory(project_path: Path) -> dict[str, object]:
    docs = safe_walk_files(project_path, DOC_EXTENSIONS)
    data = safe_walk_files(project_path, DATA_EXTENSIONS)
    databases = safe_walk_files(project_path, DB_EXTENSIONS)
    scripts = safe_walk_files(project_path, {".py", ".sql", ".yml", ".yaml"})
    size_bytes = sum(path.stat().st_size for path in safe_walk_files(project_path))
    return {
        "docs": docs,
        "data": data,
        "databases": databases,
        "scripts": scripts,
        "size_mb": round(size_bytes / 1024 / 1024, 2),
    }


@st.cache_data(show_spinner=False)
def read_text(path: Path, limit: int = 80_000) -> str:
    content = path.read_text(encoding="utf-8", errors="replace")
    return content[:limit]


@st.cache_data(show_spinner=False)
def read_table(path: Path, nrows: int = 5_000) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, nrows=nrows)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, nrows=nrows)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".json":
        return pd.read_json(path)
    return pd.DataFrame()


def git_summary(project: Project) -> dict[str, str]:
    if not (project.path / ".git").exists():
        return {"branch": "n/a", "status": "not a git repository", "latest_commit": "n/a"}
    commands = {
        "branch": ["git", "branch", "--show-current"],
        "status": ["git", "status", "--short"],
        "latest_commit": ["git", "log", "-1", "--oneline"],
    }
    output = {}
    for key, cmd in commands.items():
        try:
            result = subprocess.run(cmd, cwd=project.path, check=True, text=True, capture_output=True, timeout=10)
            output[key] = result.stdout.strip() or "clean"
        except Exception as exc:
            output[key] = f"error: {exc}"
    return output


def git_remote_url(project: Project) -> str:
    if not (project.path / ".git").exists():
        return ""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project.path,
            check=False,
            text=True,
            capture_output=True,
            timeout=10,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def display_repo_link(project: Project) -> str:
    remote = git_remote_url(project)
    return remote or relative(project.path)


def status_color(status: str) -> str:
    return "#16a34a" if status == "clean" else "#dc2626"


def inject_style() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }
        .hero {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 22px 24px;
            background: linear-gradient(135deg, #0f172a 0%, #1f2937 52%, #14532d 100%);
            color: white;
            margin-bottom: 20px;
        }
        .hero h1 {
            margin: 0 0 6px 0;
            font-size: 2.05rem;
            letter-spacing: 0;
        }
        .hero p {
            margin: 0;
            color: #d1d5db;
            font-size: 1rem;
        }
        .project-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 16px;
            min-height: 182px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
        }
        .project-title {
            font-weight: 700;
            font-size: 1rem;
            color: #111827;
            margin-bottom: 8px;
            overflow-wrap: anywhere;
        }
        .project-path {
            color: #6b7280;
            font-size: .8rem;
            margin-bottom: 12px;
            overflow-wrap: anywhere;
        }
        .status-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 3px 9px;
            color: white;
            font-size: .76rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
        }
        .card-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 10px;
        }
        .mini-metric {
            border: 1px solid #eef2f7;
            border-radius: 8px;
            padding: 8px;
            background: #f9fafb;
        }
        .mini-metric strong {
            display: block;
            color: #111827;
            font-size: 1.05rem;
        }
        .mini-metric span {
            color: #6b7280;
            font-size: .72rem;
        }
        .step {
            display: grid;
            grid-template-columns: 40px 1fr;
            gap: 12px;
            align-items: start;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px;
            background: #fff;
            margin: 9px 0;
        }
        .step strong {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: #0f766e;
            color: white;
        }
        .step p {
            margin: 3px 0 0;
        }
        @media (max-width: 1100px) {
            .card-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        @media (max-width: 720px) {
            .card-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(project_count: int, data_files: int, databases: int, docs: int) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <h1>Central Project Access Panel</h1>
            <p>{project_count} projects · {docs} documents · {data_files} data files · {databases} databases</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def database_tables(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    try:
        if suffix == ".duckdb":
            with duckdb.connect(str(path), read_only=True) as conn:
                return pd.DataFrame(conn.execute("SHOW TABLES").fetchall(), columns=["table"])
        with sqlite3.connect(path) as conn:
            return pd.read_sql_query(
                "select name as table, type from sqlite_master where type in ('table', 'view') order by name",
                conn,
            )
    except Exception as exc:
        return pd.DataFrame({"error": [str(exc)]})


def database_preview(path: Path, table: str) -> pd.DataFrame:
    suffix = path.suffix.lower()
    safe_table = table.replace('"', '""')
    if suffix == ".duckdb":
        with duckdb.connect(str(path), read_only=True) as conn:
            return conn.execute(f'SELECT * FROM "{safe_table}" LIMIT 500').fetchdf()
    with sqlite3.connect(path) as conn:
        return pd.read_sql_query(f'SELECT * FROM "{safe_table}" LIMIT 500', conn)


def service_config(project: Project) -> dict[str, object] | None:
    return PROJECT_SERVICES.get(project.name)


def service_log_dir(project: Project) -> Path:
    path = ROOT / "logs" / project.name
    path.mkdir(parents=True, exist_ok=True)
    return path


def project_venv_python(project: Project) -> Path:
    return project.path / ".venv-manager" / "bin" / "python"


def project_venv_streamlit(project: Project) -> Path:
    return project.path / ".venv-manager" / "bin" / "streamlit"


def run_background(command: list[str], cwd: Path, log_path: Path) -> None:
    with log_path.open("ab") as log:
        log.write(f"\n\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n".encode())
        log.write((" ".join(command) + "\n").encode())
        subprocess.Popen(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


def run_capture(command: list[str], cwd: Path, timeout: int = 600) -> tuple[int, str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    return result.returncode, result.stdout + result.stderr


def port_pid(port: int) -> str | None:
    try:
        result = subprocess.run(["lsof", "-ti", f":{port}"], text=True, capture_output=True, check=False)
        pid = result.stdout.strip().splitlines()
        return pid[0] if pid else None
    except Exception:
        return None


def stop_port(port: int) -> None:
    pid = port_pid(port)
    if pid:
        subprocess.run(["kill", pid], check=False)


def ensure_project_venv(project: Project) -> tuple[bool, str]:
    cfg = service_config(project)
    if not cfg:
        return False, "No service configuration for this project."
    venv_dir = project.path / ".venv-manager"
    if not project_venv_python(project).exists():
        code, output = run_capture([sys.executable, "-m", "venv", str(venv_dir)], project.path, timeout=120)
        if code != 0:
            return False, output
    requirements = project.path / str(cfg["requirements"])
    if requirements.exists():
        code, output = run_capture(
            [str(project_venv_python(project)), "-m", "pip", "install", "-r", str(requirements)],
            project.path,
            timeout=900,
        )
        return code == 0, output
    code, output = run_capture([str(project_venv_python(project)), "-m", "pip", "install", "streamlit"], project.path, timeout=300)
    return code == 0, output


def start_project_app(project: Project) -> tuple[bool, str]:
    cfg = service_config(project)
    if not cfg:
        return False, "No service configuration for this project."
    app_path = project.path / str(cfg["app"])
    port = int(cfg["port"])
    if not app_path.exists():
        return False, f"App not found: {relative(app_path)}"
    if port_pid(port):
        return True, f"Already running at http://localhost:{port}"
    streamlit_bin = project_venv_streamlit(project)
    if not streamlit_bin.exists():
        ok, output = ensure_project_venv(project)
        if not ok:
            return False, output
    log_path = service_log_dir(project) / "streamlit.log"
    run_background(
        [str(project_venv_streamlit(project)), "run", str(app_path), "--server.port", str(port), "--server.headless", "true"],
        project.path,
        log_path,
    )
    return True, f"Starting at http://localhost:{port}. Log: {relative(log_path)}"


def run_project_pipeline(project: Project) -> tuple[bool, str]:
    cfg = service_config(project)
    if not cfg or not cfg.get("pipeline"):
        return False, "No pipeline configured for this project."
    pipeline = project.path / str(cfg["pipeline"])
    if not pipeline.exists():
        return False, f"Pipeline not found: {relative(pipeline)}"
    if not project_venv_python(project).exists():
        ok, output = ensure_project_venv(project)
        if not ok:
            return False, output
    log_path = service_log_dir(project) / "pipeline.log"
    run_background([str(project_venv_python(project)), str(pipeline)], project.path, log_path)
    return True, f"Pipeline started. Log: {relative(log_path)}"


def render_log(path: Path) -> None:
    if path.exists():
        text = path.read_text(encoding="utf-8", errors="replace")
        st.code(text[-12_000:] if text else "Log is empty.")
    else:
        st.info("No log yet.")


def render_project_cards(projects: list[Project]) -> None:
    rows = []
    for project in projects:
        inv = project_inventory(project.path)
        git = git_summary(project)
        rows.append(
            {
                "project": project.name,
                "branch": git["branch"],
                "status": "dirty" if git["status"] != "clean" else "clean",
                "docs": len(inv["docs"]),
                "data_files": len(inv["data"]),
                "databases": len(inv["databases"]),
                "size_mb": inv["size_mb"],
                "path": relative(project.path),
                "repo": display_repo_link(project),
                "url": f"http://localhost:{service_config(project)['port']}" if service_config(project) else "n/a",
                "running": bool(port_pid(int(service_config(project)["port"]))) if service_config(project) else False,
            }
        )
    html = ['<div class="card-grid">']
    for row in rows:
        color = status_color(row["status"])
        html.append(
            f"""
            <div class="project-card">
                <div class="status-pill" style="background:{color}">{row["status"]}</div>
                <div class="project-title">{row["project"]}</div>
                <div class="project-path">{row["path"]}</div>
                <div class="project-path">repo: {row["repo"]}</div>
                <div class="project-path">dashboard: {row["url"]} · {'running' if row["running"] else 'stopped'}</div>
                <div class="card-metrics">
                    <div class="mini-metric"><strong>{row["docs"]}</strong><span>docs</span></div>
                    <div class="mini-metric"><strong>{row["data_files"]}</strong><span>data</span></div>
                    <div class="mini-metric"><strong>{row["databases"]}</strong><span>databases</span></div>
                </div>
                <div class="project-path" style="margin-top:12px">branch: {row["branch"]} · {row["size_mb"]} MB</div>
            </div>
            """
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_academy() -> None:
    render_hero(len(list_projects()), 0, 0, len(ACADEMY_TOPICS))
    st.subheader("Step-by-step learning center")
    topic = st.selectbox("Topic", list(ACADEMY_TOPICS))
    content = ACADEMY_TOPICS[topic]
    st.markdown(f"### {topic}")
    st.info(content["purpose"])
    for idx, step in enumerate(content["steps"], start=1):
        st.markdown(
            f"""
            <div class="step">
                <strong>{idx}</strong>
                <p>{step}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.success(content["result"])

    st.subheader("Where this appears in the projects")
    mapping = pd.DataFrame(
        [
            {"topic": "Git", "examples": "Every repository inside projects/"},
            {"topic": "dbt", "examples": "fuel, retail, tyrewear, citibike"},
            {"topic": "Relational SQLite", "examples": "retail_analytics_learning_repo, retail_case_repo"},
            {"topic": "DuckDB", "examples": "fuel, retail, tyrewear"},
            {"topic": "Statistical Analysis", "examples": "fuel, citibike, portugal bike, tyrewear"},
            {"topic": "Machine Learning", "examples": "fuel, retail, portugal bike, citibike, tyrewear"},
            {"topic": "Streamlit", "examples": "project apps and this central dashboard"},
            {"topic": "Results", "examples": "data/outputs, docs, docs_html, dashboards"},
        ]
    )
    st.dataframe(mapping, width="stretch", hide_index=True)


def render_access_links(projects: list[Project]) -> None:
    st.subheader("Dashboard access panel")
    rows = []
    for project in projects:
        cfg = service_config(project)
        context = PROJECT_CONTEXT.get(project.name, {})
        if not cfg:
            continue
        port = int(cfg["port"])
        rows.append(
            {
                "project": context.get("title", project.name),
                "folder": relative(project.path),
                "repository": display_repo_link(project),
                "dashboard": f"http://localhost:{port}",
                "service_status": "running" if port_pid(port) else "stopped",
                "app_entrypoint": cfg["app"],
                "pipeline": cfg["pipeline"] or "n/a",
            }
        )
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    cols = st.columns(3)
    for idx, row in enumerate(rows):
        with cols[idx % 3]:
            st.markdown(f"**{row['project']}**")
            st.caption(row["folder"])
            if row["repository"].startswith("http"):
                st.link_button("Open repository", row["repository"])
            else:
                st.caption(f"Local repository: {row['repository']}")
            st.link_button("Open dashboard", row["dashboard"], disabled=row["service_status"] != "running")


def render_project_context(project: Project) -> None:
    context = PROJECT_CONTEXT.get(project.name)
    if not context:
        st.info("No extended project context registered yet.")
        return
    cfg = service_config(project)
    dashboard = f"http://localhost:{cfg['port']}" if cfg else "n/a"
    repository = display_repo_link(project)
    st.subheader(context["title"])
    if repository.startswith("http"):
        st.link_button("Open repository", repository)
    else:
        st.caption(f"Local repository: {repository}")
    st.link_button("Open project dashboard", dashboard, disabled=not (cfg and port_pid(int(cfg["port"]))))
    sections = [
        ("Creation and purpose", "creation"),
        ("Business / analytical context", "context"),
        ("Programming and code structure", "programming"),
        ("Mathematics and statistics", "math"),
        ("Machine learning", "ml"),
        ("Results and interpretation", "results"),
    ]
    for title, key in sections:
        with st.expander(title, expanded=True):
            st.write(context[key])


def render_theory() -> None:
    content = THEORY["en"]
    st.markdown(f"## {content['title']}")
    st.write(content["intro"])
    for topic, details in content["topics"].items():
        with st.expander(topic, expanded=True):
            st.markdown("**Formula**")
            st.code(details["formula"])
            st.markdown("**Example**")
            st.write(details["example"])
            st.markdown("**Use in projects**")
            st.write(details["use"])


def render_project_service(project: Project) -> None:
    cfg = service_config(project)
    if not cfg:
        st.info("This project does not have a configured service yet.")
        return
    port = int(cfg["port"])
    pid = port_pid(port)
    url = f"http://localhost:{port}"
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Port", port)
    c2.metric("Status", "running" if pid else "stopped")
    c3.metric("PID", pid or "n/a")
    c4.link_button("Open App", url, disabled=not bool(pid))

    b1, b2, b3, b4 = st.columns(4)
    if b1.button("Install / Update Dependencies", key=f"install-{project.name}"):
        with st.spinner("Installing dependencies..."):
            ok, output = ensure_project_venv(project)
        st.success("Dependencies ready.") if ok else st.error("Dependency install failed.")
        st.code(output[-12_000:])
    if b2.button("Start App", key=f"start-{project.name}"):
        ok, message = start_project_app(project)
        st.success(message) if ok else st.error(message)
    if b3.button("Stop App", key=f"stop-{project.name}", disabled=not bool(pid)):
        stop_port(port)
        st.success(f"Stopped service on port {port}.")
    if b4.button("Run Pipeline", key=f"pipeline-{project.name}", disabled=not bool(cfg.get("pipeline"))):
        ok, message = run_project_pipeline(project)
        st.success(message) if ok else st.error(message)

    st.subheader("Service log")
    render_log(service_log_dir(project) / "streamlit.log")
    st.subheader("Pipeline log")
    render_log(service_log_dir(project) / "pipeline.log")


def render_services(projects: list[Project]) -> None:
    st.subheader("Project services")
    rows = []
    for project in projects:
        cfg = service_config(project)
        if not cfg:
            continue
        port = int(cfg["port"])
        rows.append(
            {
                "project": project.name,
                "app": cfg["app"],
                "pipeline": cfg["pipeline"] or "n/a",
                "port": port,
                "url": f"http://localhost:{port}",
                "status": "running" if port_pid(port) else "stopped",
            }
        )
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    selected = st.selectbox("Project", [project for project in projects if service_config(project)], format_func=lambda project: project.name)
    render_project_service(selected)


def render_html_docs() -> None:
    st.subheader("Central HTML documentation")
    docs = safe_walk_files(DOCS_HTML_DIR, {".html"}) if DOCS_HTML_DIR.exists() else []
    if not docs:
        st.info("No central HTML pages found.")
        return
    selected = st.selectbox("Page", docs, format_func=relative)
    st.components.v1.html(read_text(selected, limit=350_000), height=760, scrolling=True)


def render_results_center(projects: list[Project]) -> None:
    st.subheader("Results center")
    rows = []
    for project in projects:
        inv = project_inventory(project.path)
        output_files = [path for path in inv["data"] if "output" in relative(path).lower() or "processed" in relative(path).lower()]
        rows.append(
            {
                "project": project.name,
                "data_files": len(inv["data"]),
                "output_or_processed": len(output_files),
                "databases": len(inv["databases"]),
                "docs": len(inv["docs"]),
                "size_mb": inv["size_mb"],
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(df, width="stretch", hide_index=True)
    fig = px.scatter(
        df,
        x="data_files",
        y="docs",
        size="size_mb",
        color="databases",
        hover_name="project",
        title="Projects by data files, documentation and databases",
        color_continuous_scale="Tealgrn",
    )
    fig.update_layout(height=430)
    st.plotly_chart(fig, width="stretch")


def project_summary_frame(projects: list[Project]) -> pd.DataFrame:
    rows = []
    for project in projects:
        inv = project_inventory(project.path)
        git = git_summary(project)
        rows.append(
            {
                "project": project.name,
                "docs": len(inv["docs"]),
                "data": len(inv["data"]),
                "databases": len(inv["databases"]),
                "scripts": len(inv["scripts"]),
                "size_mb": inv["size_mb"],
                "status": "dirty" if git["status"] != "clean" else "clean",
            }
        )
    return pd.DataFrame(rows)


def render_visual_summary(projects: list[Project]) -> None:
    summary = project_summary_frame(projects)
    render_hero(
        len(projects),
        int(summary["data"].sum()),
        int(summary["databases"].sum()),
        int(summary["docs"].sum()),
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projects", len(projects))
    c2.metric("Documents", int(summary["docs"].sum()))
    c3.metric("Data Files", int(summary["data"].sum()))
    c4.metric("Databases", int(summary["databases"].sum()))

    left, right = st.columns([1.4, 1])
    with left:
        fig = px.bar(
            summary.sort_values("data", ascending=False),
            x="project",
            y=["docs", "data", "databases", "scripts"],
            barmode="group",
            title="Project inventory",
            color_discrete_sequence=["#2563eb", "#16a34a", "#dc2626", "#9333ea"],
        )
        fig.update_layout(height=390, legend_title_text="", xaxis_title="", yaxis_title="files")
        st.plotly_chart(fig, width="stretch")
    with right:
        totals = {
            "Docs": int(summary["docs"].sum()),
            "Data": int(summary["data"].sum()),
            "Databases": int(summary["databases"].sum()),
            "Scripts": int(summary["scripts"].sum()),
        }
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(totals),
                    values=list(totals.values()),
                    hole=0.55,
                    marker_colors=["#2563eb", "#16a34a", "#dc2626", "#9333ea"],
                )
            ]
        )
        fig.update_layout(title="Overall composition", height=390, showlegend=True)
        st.plotly_chart(fig, width="stretch")

    st.subheader("Projects")
    render_project_cards(projects)
    render_access_links(projects)


def render_docs(project: Project) -> None:
    docs = project_inventory(project.path)["docs"]
    if not docs:
        st.info("No documentation found for this project.")
        return
    selected = st.selectbox("Document", docs, format_func=relative)
    if selected.suffix.lower() == ".md":
        st.markdown(read_text(selected))
    elif selected.suffix.lower() in {".html", ".htm"}:
        st.components.v1.html(read_text(selected, limit=250_000), height=700, scrolling=True)
    else:
        st.write(relative(selected))
        st.code(read_text(selected, limit=20_000) if selected.suffix.lower() == ".txt" else "PDF available at the path above.")


def render_data(project: Project) -> None:
    files = project_inventory(project.path)["data"]
    if not files:
        st.info("No tabular data files found.")
        return
    selected = st.selectbox("Data file", files, format_func=relative)
    df = read_table(selected)
    st.caption(f"{relative(selected)} · {len(df):,} loaded rows")
    st.dataframe(df.head(500), width="stretch", hide_index=True)
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        cols = st.columns(3)
        x_options = ["index"] + list(df.columns)
        x_col = cols[0].selectbox("X axis", x_options)
        y_col = cols[1].selectbox("Y axis", list(numeric.columns))
        chart_type = cols[2].selectbox("Chart", ["Line", "Bar", "Scatter", "Histogram"])
        chart_df = df.reset_index(names="index")
        if chart_type == "Line":
            fig = px.line(chart_df, x=x_col, y=y_col)
        elif chart_type == "Bar":
            fig = px.bar(chart_df.head(100), x=x_col, y=y_col)
        elif chart_type == "Scatter":
            fig = px.scatter(chart_df, x=x_col, y=y_col)
        else:
            fig = px.histogram(chart_df, x=y_col)
        st.plotly_chart(fig, width="stretch")


def render_databases(project: Project) -> None:
    databases = project_inventory(project.path)["databases"]
    if not databases:
        st.info("No DuckDB/SQLite databases found.")
        return
    selected = st.selectbox("Database", databases, format_func=relative)
    tables = database_tables(selected)
    st.dataframe(tables, width="stretch", hide_index=True)
    if "table" in tables.columns and not tables.empty:
        table = st.selectbox("Tabela/View", tables["table"].tolist())
        preview = database_preview(selected, table)
        st.dataframe(preview, width="stretch", hide_index=True)


def render_status(project: Project) -> None:
    git = git_summary(project)
    st.metric("Branch", git["branch"])
    st.code(git["latest_commit"])
    st.subheader("Git Status")
    st.code(git["status"])
    changelog = project.path / "CHANGELOG.md"
    if changelog.exists():
        st.subheader("Changelog")
        st.markdown(read_text(changelog))


def main() -> None:
    st.set_page_config(page_title="Central Project Access Panel", layout="wide")
    inject_style()

    projects = list_projects()
    if not projects:
        st.warning("No projects found in `projects/`.")
        return

    page = st.sidebar.radio("View", ["Access Panel", "Services", "Academy", "Theory", "Central HTML", "Results", "Project", "Materials", "Global Changelog"])

    if page == "Access Panel":
        render_visual_summary(projects)
        return

    if page == "Services":
        render_services(projects)
        return

    if page == "Academy":
        render_academy()
        return

    if page == "Theory":
        render_theory()
        return

    if page == "Central HTML":
        render_html_docs()
        return

    if page == "Results":
        render_results_center(projects)
        return

    if page == "Materials":
        st.subheader("Learning materials")
        materials = safe_walk_files(LEARNING_DIR) if LEARNING_DIR.exists() else []
        st.dataframe(pd.DataFrame({"file": [relative(path) for path in materials]}), width="stretch", hide_index=True)
        return

    if page == "Global Changelog":
        st.subheader("Global changelog")
        changelog = ROOT / "CHANGELOG.md"
        st.markdown(read_text(changelog) if changelog.exists() else "No global changelog.")
        return

    project = st.sidebar.selectbox("Project", projects, format_func=lambda item: item.name)
    inv = project_inventory(project.path)
    st.markdown(
        f"""
        <div class="hero">
            <h1>{project.name}</h1>
            <p>{len(inv["docs"])} documents · {len(inv["data"])} data files · {len(inv["databases"])} databases · {inv["size_mb"]} MB</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    tab_overview, tab_status, tab_run, tab_docs, tab_data, tab_db = st.tabs(["Overview", "Status", "Run", "Documentation", "Data & Charts", "Databases"])
    with tab_overview:
        render_project_context(project)
    with tab_status:
        render_status(project)
    with tab_run:
        render_project_service(project)
    with tab_docs:
        render_docs(project)
    with tab_data:
        render_data(project)
    with tab_db:
        render_databases(project)


if __name__ == "__main__":
    main()
