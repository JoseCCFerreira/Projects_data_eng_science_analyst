import streamlit as st
import pandas as pd
from src.quality.missing_values import missing_value_summary
from src.quality.outlier_detection import detect_iqr_outliers
from src.utils.paths import RAW_CSV
from streamlit_app.components.charts import box_plot

st.title("Data Quality")

df = pd.read_csv(RAW_CSV, parse_dates=["timestamp"], dayfirst=False)

st.subheader("Missing Values")
missing = missing_value_summary(df)
st.table(missing)

st.subheader("Duplicados")
st.write(f"Total de duplicados: {df.duplicated().sum()}")

st.subheader("Outliers (IQR)")
outliers = detect_iqr_outliers(df, ["temperature", "humidity", "pressure", "vibration", "energy_consumption"])
st.table(outliers)

st.subheader("Qualidade por sensor")
quality_sensor = df.groupby("sensor_id").agg({"temperature": "count", "timestamp": "nunique"}).reset_index()
st.dataframe(quality_sensor)

st.subheader("Boxplot de temperatura")
st.plotly_chart(box_plot(df, "temperature", x="machine_id", title="Temperatura por máquina"))
