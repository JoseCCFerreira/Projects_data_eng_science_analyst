import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st

st.set_page_config(page_title="Data Quality ML Pipeline", layout="wide")

st.title("Data Quality & ML Pipeline")
st.markdown(
    "Este projeto demonstra um fluxo completo de dados industriais: geração, armazenamento, dbt, qualidade, ML e visualização interativa."
)
st.markdown("Use o menu lateral para navegar entre as páginas de overview, data quality, análise estatística, clustering e previsão.")

st.header("Resumo do projeto")
st.write(
    "A estrutura deste projeto inclui SQLite transacional, DuckDB analítico, modelos dbt, limpeza, resampling, filtragem, clustering, predição e um dashboard Streamlit." 
)

st.markdown("### Passos rápidos")
st.markdown(
    "1. Gere os dados com `make generate-data`\n"
    "2. Carregue SQLite e DuckDB com `make load-sqlite` e `make load-duckdb`\n"
    "3. Execute dbt com `make dbt-run` e `make dbt-test`\n"
    "4. Verifique qualidade, ML e dashboards." 
)
