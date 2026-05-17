import streamlit as st
import pandas as pd
from src.utils.paths import CLUSTERING_EXPORT
from streamlit_app.components.charts import scatter

st.title("Clustering")

df = pd.read_csv(CLUSTERING_EXPORT)

st.subheader("Distribuição dos grupos")
st.write(df[[col for col in df.columns if col.startswith("cluster_")]].head())

st.subheader("PCA 2D")
st.plotly_chart(scatter(df, "pca_1", "pca_2", color="cluster_kmeans", title="KMeans PCA Clusters"))

st.subheader("Clusters por máquina")
st.write(df.groupby(["machine_id", "cluster_kmeans"]).size().reset_index(name="count"))
