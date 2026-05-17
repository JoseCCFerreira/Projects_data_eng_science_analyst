import streamlit as st
import pandas as pd
from src.utils.paths import PREDICTION_EXPORT
from streamlit_app.components.charts import scatter

st.title("Predictions")

df = pd.read_csv(PREDICTION_EXPORT)

st.subheader("Métricas e resultados")
st.write(df.head())

if "pred_rf" in df.columns:
    st.subheader("Real vs Previsto")
    st.plotly_chart(scatter(df, "target_failure_risk", "pred_rf", title="Real vs Predicted Failure Risk"))

st.subheader("Importância das variáveis")
st.write("Os modelos foram salvos na pasta `models/predictive`. Para ver a importância exata, extraia o RandomForest e calcule `feature_importances_`.")
