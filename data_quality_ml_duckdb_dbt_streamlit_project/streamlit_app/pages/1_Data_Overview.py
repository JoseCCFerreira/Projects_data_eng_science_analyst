import streamlit as st
import pandas as pd
from src.utils.paths import RAW_CSV
from streamlit_app.components.charts import histogram

st.title("Data Overview")

df = pd.read_csv(RAW_CSV, parse_dates=["timestamp"], dayfirst=False)

st.metric("Linhas", len(df))
st.metric("Sensores", df["sensor_id"].nunique())
st.metric("Máquinas", df["machine_id"].nunique())
st.metric("Intervalo", f"{df['timestamp'].min()} a {df['timestamp'].max()}")

st.subheader("Estatísticas Principais")
st.dataframe(df.describe(include='all').transpose())

st.subheader("Distribuição de energia")
st.plotly_chart(histogram(df, "energy_consumption", "Energy Consumption Distribution"))
