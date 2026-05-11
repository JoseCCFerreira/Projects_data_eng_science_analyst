from __future__ import annotations

import sqlite3
import subprocess
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

    page = st.sidebar.radio("Vista", ["Resumo", "Academia", "HTML Central", "Resultados", "Projeto", "Materiais", "Registo Global"])

    if page == "Resumo":
        render_visual_summary(projects)
        return

    if page == "Academia":
        render_academy()
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
    tab_status, tab_docs, tab_data, tab_db = st.tabs(["Estado", "Documentação", "Dados & Gráficos", "Bases de Dados"])
    with tab_status:
        render_status(project)
    with tab_docs:
        render_docs(project)
    with tab_data:
        render_data(project)
    with tab_db:
        render_databases(project)


if __name__ == "__main__":
    main()
