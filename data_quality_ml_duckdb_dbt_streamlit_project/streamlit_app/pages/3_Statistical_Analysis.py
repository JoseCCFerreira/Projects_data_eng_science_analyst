import streamlit as st
import pandas as pd
from src.quality.statistical_profiling import correlation_matrix
from src.utils.paths import RAW_CSV
from streamlit_app.components.charts import heatmap, histogram, line_chart

st.title("Statistical Analysis")

df = pd.read_csv(RAW_CSV, parse_dates=["timestamp"], dayfirst=False)

st.subheader("Histogramas")
st.plotly_chart(histogram(df, "temperature", "Temperature Distribution"))

st.subheader("Correlação")
corr = correlation_matrix(df)
st.plotly_chart(heatmap(corr, "Correlation Matrix"))

st.subheader("Tendência temporal de energia")
energy_trend = df.set_index("timestamp").resample("D")["energy_consumption"].mean().reset_index()
st.plotly_chart(line_chart(energy_trend, "timestamp", "energy_consumption", title="Daily Energy Consumption"))
