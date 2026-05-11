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
        "purpose": "Controlar versoes, commits, historico e recuperacao.",
        "steps": [
            "Ver o estado antes de mexer: git status --short.",
            "Ler as alteracoes: git diff.",
            "Agrupar trabalho pequeno: git add ficheiros.",
            "Guardar com contexto: git commit -m \"mensagem clara\".",
            "Consultar historico: git log --oneline.",
        ],
        "result": "Um historico limpo onde cada commit explica uma decisao tecnica.",
    },
    "dbt": {
        "purpose": "Transformar dados com SQL organizado, testavel e documentado.",
        "steps": [
            "Carregar fontes raw em DuckDB ou warehouse.",
            "Criar staging models para limpar nomes, tipos e granularidade.",
            "Criar intermediate models para joins e regras de negocio.",
            "Criar marts para responder a perguntas finais.",
            "Executar dbt build para correr modelos e testes.",
        ],
        "result": "Uma camada analitica com linhagem, SQL legivel e testes de qualidade.",
    },
    "SQLite Relacional": {
        "purpose": "Representar operacoes transacionais com tabelas relacionadas.",
        "steps": [
            "Separar entidades: clientes, produtos, lojas, transacoes.",
            "Definir primary keys e foreign keys.",
            "Criar indices para consultas frequentes.",
            "Consultar com joins, where, group by e window functions quando fizer sentido.",
            "Usar SQLite para ensino, apps pequenas e exemplos OLTP.",
        ],
        "result": "Uma base compacta que ensina integridade relacional e consultas SQL.",
    },
    "DuckDB": {
        "purpose": "Fazer analise local rapida sobre CSV, Parquet e tabelas grandes.",
        "steps": [
            "Ler ficheiros diretamente ou materializar tabelas.",
            "Criar views analiticas por tema.",
            "Agregacoes e joins pesados passam para DuckDB.",
            "Servir dados para Python, dbt e Streamlit.",
            "Guardar snapshots reproduciveis em .duckdb quando necessario.",
        ],
        "result": "Um motor OLAP local para explorar resultados sem servidor externo.",
    },
    "Statistical Analysis": {
        "purpose": "Transformar dados em sinais medidos: distribuicao, variacao, risco e relacoes.",
        "steps": [
            "Ver cobertura temporal e missing values.",
            "Calcular medias, medianas, desvios e quantis.",
            "Analisar volatilidade, outliers e z-scores.",
            "Medir correlacoes e estudos de eventos.",
            "Documentar limites antes de sugerir causalidade.",
        ],
        "result": "Conclusoes mais honestas, com sinal separado de ruido.",
    },
    "Machine Learning": {
        "purpose": "Aprender padroes para previsao, classificacao ou ranking.",
        "steps": [
            "Definir target e features sem fuga de informacao.",
            "Separar treino e teste, idealmente respeitando tempo quando e serie temporal.",
            "Treinar baseline e modelo principal.",
            "Medir erro, estabilidade e importancia de features.",
            "Explicar quando o modelo deve ou nao ser usado.",
        ],
        "result": "Modelos avaliados, nao apenas treinados.",
    },
    "Streamlit": {
        "purpose": "Transformar dados e modelos numa experiencia interativa.",
        "steps": [
            "Carregar dados de CSV, SQLite ou DuckDB.",
            "Criar filtros e seletores para a pergunta do utilizador.",
            "Mostrar metricas, tabelas, graficos e downloads.",
            "Separar paginas por fluxo de trabalho.",
            "Usar cache para tornar a app rapida.",
        ],
        "result": "Uma interface pratica para explorar o projeto sem abrir codigo.",
    },
    "Resultados": {
        "purpose": "Fechar o ciclo entre dados, graficos, interpretacao e decisao.",
        "steps": [
            "Gerar outputs reproduziveis.",
            "Validar linhas, colunas e metricas.",
            "Criar graficos que respondem a perguntas claras.",
            "Escrever conclusoes com metodologia e limites.",
            "Registar alteracoes no changelog.",
        ],
        "result": "Um resultado explicavel de ponta a ponta.",
    },
}

THEORY = {
    "pt": {
        "title": "Teoria matematica e estatistica",
        "intro": "Esta secao liga as formulas aos projetos. A ideia e perceber o que cada metrica mede, quando usar e como interpretar.",
        "topics": {
            "Media, variancia e desvio padrao": {
                "formula": "media = soma(x_i) / n; variancia = soma((x_i - media)^2) / (n - 1); desvio = sqrt(variancia)",
                "example": "Se os crescimentos mensais forem [2, -1, 4, 0], a media e 1.25. O desvio padrao mede quanto os meses se afastam dessa media.",
                "use": "Usado em volatilidade de combustiveis, vendas medias no retail e distribuicao de utilizacao de bicicletas.",
            },
            "Z-score e outliers": {
                "formula": "z = (x - media) / desvio_padrao",
                "example": "Um z-score de 2.8 significa que o valor esta 2.8 desvios padrao acima do comportamento medio.",
                "use": "No projeto fuel, price_jump_flag marca choques quando a mudanca mensal tem z-score absoluto elevado.",
            },
            "Correlacao": {
                "formula": "corr(X,Y) = cov(X,Y) / (std(X) * std(Y))",
                "example": "Se preco do fuel e conflito sobem juntos, a correlacao pode ser positiva. Mas correlacao nao prova causalidade.",
                "use": "Matrizes de correlacao nos projetos fuel, tyrewear, retail e citibike.",
            },
            "Regressao linear": {
                "formula": "y = beta_0 + beta_1*x_1 + ... + erro",
                "example": "Prever vendas usando preco, desconto e sazonalidade. beta_1 indica quanto y muda quando x_1 aumenta uma unidade.",
                "use": "Baseline interpretavel antes de modelos mais complexos.",
            },
            "Classificacao e matriz de confusao": {
                "formula": "accuracy = acertos / total; precision = TP/(TP+FP); recall = TP/(TP+FN)",
                "example": "Num modelo que deteta choque de preco, falso positivo e avisar choque sem choque; falso negativo e falhar um choque real.",
                "use": "Modelos de risco, fraude, churn ou price jump.",
            },
            "Series temporais": {
                "formula": "retorno_t = (valor_t / valor_{t-1} - 1) * 100",
                "example": "Se o preco passa de 100 para 110, o retorno e 10%. Se passa de 110 para 99, o retorno e -10%.",
                "use": "Fuel forecasting, evolucao de vendas, procura por bicicletas e desgaste temporal.",
            },
            "Clustering": {
                "formula": "distancia euclidiana = sqrt(soma((x_i - y_i)^2))",
                "example": "Agrupar lojas parecidas por vendas, margem e numero de clientes.",
                "use": "Segmentacao em retail, pneus, mobilidade e padroes de uso.",
            },
        },
    },
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
            <h1>Projecto Manager</h1>
            <p>{project_count} projetos · {docs} documentos · {data_files} ficheiros de dados · {databases} bases de dados</p>
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
                <div class="card-metrics">
                    <div class="mini-metric"><strong>{row["docs"]}</strong><span>docs</span></div>
                    <div class="mini-metric"><strong>{row["data_files"]}</strong><span>dados</span></div>
                    <div class="mini-metric"><strong>{row["databases"]}</strong><span>bases</span></div>
                </div>
                <div class="project-path" style="margin-top:12px">branch: {row["branch"]} · {row["size_mb"]} MB</div>
            </div>
            """
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_academy() -> None:
    render_hero(len(list_projects()), 0, 0, len(ACADEMY_TOPICS))
    st.subheader("Academia timtim por timtim")
    topic = st.selectbox("Tema", list(ACADEMY_TOPICS))
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

    st.subheader("Onde isto aparece nos teus projetos")
    mapping = pd.DataFrame(
        [
            {"tema": "Git", "exemplos": "Todos os repositorios em projects/"},
            {"tema": "dbt", "exemplos": "fuel, retail, tyrewear, citibike"},
            {"tema": "SQLite Relacional", "exemplos": "retail_analytics_learning_repo, retail_case_repo"},
            {"tema": "DuckDB", "exemplos": "fuel, retail, tyrewear"},
            {"tema": "Statistical Analysis", "exemplos": "fuel, citibike, portugal bike, tyrewear"},
            {"tema": "Machine Learning", "exemplos": "fuel, retail, portugal bike, citibike, tyrewear"},
            {"tema": "Streamlit", "exemplos": "apps dos projetos e esta dashboard central"},
            {"tema": "Resultados", "exemplos": "data/outputs, docs, docs_html, dashboards"},
        ]
    )
    st.dataframe(mapping, width="stretch", hide_index=True)


def render_theory() -> None:
    language = st.radio("Language / Idioma", ["pt", "en"], horizontal=True, format_func=lambda value: "Português" if value == "pt" else "English")
    content = THEORY[language]
    st.markdown(f"## {content['title']}")
    st.write(content["intro"])
    for topic, details in content["topics"].items():
        with st.expander(topic, expanded=True):
            st.markdown("**Formula**")
            st.code(details["formula"])
            st.markdown("**Example / Exemplo**")
            st.write(details["example"])
            st.markdown("**Use in projects / Uso nos projetos**")
            st.write(details["use"])


def render_project_service(project: Project) -> None:
    cfg = service_config(project)
    if not cfg:
        st.info("Este projeto ainda nao tem servico configurado no manager.")
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
    st.subheader("Servicos dos projetos")
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
    selected = st.selectbox("Projeto", [project for project in projects if service_config(project)], format_func=lambda project: project.name)
    render_project_service(selected)


def render_html_docs() -> None:
    st.subheader("Documentacao HTML central")
    docs = safe_walk_files(DOCS_HTML_DIR, {".html"}) if DOCS_HTML_DIR.exists() else []
    if not docs:
        st.info("Sem paginas HTML centrais.")
        return
    selected = st.selectbox("Pagina", docs, format_func=relative)
    st.components.v1.html(read_text(selected, limit=350_000), height=760, scrolling=True)


def render_results_center(projects: list[Project]) -> None:
    st.subheader("Centro de resultados")
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
        title="Projetos por dados, documentacao e bases",
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
    c1.metric("Projetos", len(projects))
    c2.metric("Documentos", int(summary["docs"].sum()))
    c3.metric("Ficheiros de Dados", int(summary["data"].sum()))
    c4.metric("Bases de Dados", int(summary["databases"].sum()))

    left, right = st.columns([1.4, 1])
    with left:
        fig = px.bar(
            summary.sort_values("data", ascending=False),
            x="project",
            y=["docs", "data", "databases", "scripts"],
            barmode="group",
            title="Inventário por projeto",
            color_discrete_sequence=["#2563eb", "#16a34a", "#dc2626", "#9333ea"],
        )
        fig.update_layout(height=390, legend_title_text="", xaxis_title="", yaxis_title="ficheiros")
        st.plotly_chart(fig, width="stretch")
    with right:
        totals = {
            "Docs": int(summary["docs"].sum()),
            "Dados": int(summary["data"].sum()),
            "Bases": int(summary["databases"].sum()),
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
        fig.update_layout(title="Composição geral", height=390, showlegend=True)
        st.plotly_chart(fig, width="stretch")

    st.subheader("Projetos")
    render_project_cards(projects)


def render_docs(project: Project) -> None:
    docs = project_inventory(project.path)["docs"]
    if not docs:
        st.info("Sem documentação encontrada neste projeto.")
        return
    selected = st.selectbox("Documento", docs, format_func=relative)
    if selected.suffix.lower() == ".md":
        st.markdown(read_text(selected))
    elif selected.suffix.lower() in {".html", ".htm"}:
        st.components.v1.html(read_text(selected, limit=250_000), height=700, scrolling=True)
    else:
        st.write(relative(selected))
        st.code(read_text(selected, limit=20_000) if selected.suffix.lower() == ".txt" else "PDF disponível no caminho acima.")


def render_data(project: Project) -> None:
    files = project_inventory(project.path)["data"]
    if not files:
        st.info("Sem ficheiros de dados tabulares encontrados.")
        return
    selected = st.selectbox("Ficheiro de dados", files, format_func=relative)
    df = read_table(selected)
    st.caption(f"{relative(selected)} · {len(df):,} linhas carregadas")
    st.dataframe(df.head(500), width="stretch", hide_index=True)
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        cols = st.columns(3)
        x_options = ["index"] + list(df.columns)
        x_col = cols[0].selectbox("Eixo X", x_options)
        y_col = cols[1].selectbox("Eixo Y", list(numeric.columns))
        chart_type = cols[2].selectbox("Gráfico", ["Linha", "Barras", "Dispersão", "Histograma"])
        chart_df = df.reset_index(names="index")
        if chart_type == "Linha":
            fig = px.line(chart_df, x=x_col, y=y_col)
        elif chart_type == "Barras":
            fig = px.bar(chart_df.head(100), x=x_col, y=y_col)
        elif chart_type == "Dispersão":
            fig = px.scatter(chart_df, x=x_col, y=y_col)
        else:
            fig = px.histogram(chart_df, x=y_col)
        st.plotly_chart(fig, width="stretch")


def render_databases(project: Project) -> None:
    databases = project_inventory(project.path)["databases"]
    if not databases:
        st.info("Sem bases DuckDB/SQLite encontradas.")
        return
    selected = st.selectbox("Base de dados", databases, format_func=relative)
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
    st.set_page_config(page_title="Projecto Manager", layout="wide")
    inject_style()

    projects = list_projects()
    if not projects:
        st.warning("Não encontrei projetos em `projects/`.")
        return

    page = st.sidebar.radio("Vista", ["Resumo", "Serviços", "Academia", "Teoria", "HTML Central", "Resultados", "Projeto", "Materiais", "Registo Global"])

    if page == "Resumo":
        render_visual_summary(projects)
        return

    if page == "Serviços":
        render_services(projects)
        return

    if page == "Academia":
        render_academy()
        return

    if page == "Teoria":
        render_theory()
        return

    if page == "HTML Central":
        render_html_docs()
        return

    if page == "Resultados":
        render_results_center(projects)
        return

    if page == "Materiais":
        st.subheader("Materiais de estudo")
        materials = safe_walk_files(LEARNING_DIR) if LEARNING_DIR.exists() else []
        st.dataframe(pd.DataFrame({"file": [relative(path) for path in materials]}), width="stretch", hide_index=True)
        return

    if page == "Registo Global":
        st.subheader("Registo global")
        changelog = ROOT / "CHANGELOG.md"
        st.markdown(read_text(changelog) if changelog.exists() else "Sem changelog global.")
        return

    project = st.sidebar.selectbox("Projeto", projects, format_func=lambda item: item.name)
    inv = project_inventory(project.path)
    st.markdown(
        f"""
        <div class="hero">
            <h1>{project.name}</h1>
            <p>{len(inv["docs"])} documentos · {len(inv["data"])} dados · {len(inv["databases"])} bases · {inv["size_mb"]} MB</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    tab_status, tab_run, tab_docs, tab_data, tab_db = st.tabs(["Estado", "Executar", "Documentação", "Dados & Gráficos", "Bases de Dados"])
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
