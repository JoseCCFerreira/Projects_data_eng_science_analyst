import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from src.ml.model_evaluation import regression_metrics
from src.utils.paths import CLEAN_CSV, PREDICTION_EXPORT
from src.utils.logging_config import logger


def build_dataset(df: pd.DataFrame):
    features = ["temperature", "humidity", "pressure", "vibration", "energy_consumption"]
    X = df[features].copy()
    y = df["target_failure_risk"].copy()
    return X, y


def main():
    df = pd.read_csv(CLEAN_CSV, parse_dates=["timestamp"], dayfirst=False)
    df = df.dropna(subset=["target_failure_risk"])
    X, y = build_dataset(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    lr = LinearRegression()
    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    lr.fit(X_train, y_train)
    rf.fit(X_train, y_train)

    pred_lr = lr.predict(X_test)
    pred_rf = rf.predict(X_test)

    metrics_lr = regression_metrics(y_test, pred_lr)
    metrics_rf = regression_metrics(y_test, pred_rf)

    model_dir = Path(__file__).resolve().parents[2] / "models" / "predictive"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(lr, model_dir / "linear_regression.joblib")
    joblib.dump(rf, model_dir / "random_forest.joblib")

    export_df = X_test.copy()
    export_df["target_failure_risk"] = y_test
    export_df["pred_lr"] = pred_lr
    export_df["pred_rf"] = pred_rf
    PREDICTION_EXPORT.parent.mkdir(parents=True, exist_ok=True)
    export_df.to_csv(PREDICTION_EXPORT, index=False)

    report_path = Path(__file__).resolve().parents[2] / "reports" / "ml_results_report.md"
    with open(report_path, "a") as f:
        f.write("\n## Predictive Modeling\n")
        f.write("### Linear Regression\n")
        for k, v in metrics_lr.items():
            f.write(f"- {k}: {v:.4f}\n")
        f.write("### Random Forest Regressor\n")
        for k, v in metrics_rf.items():
            f.write(f"- {k}: {v:.4f}\n")
        f.write("\n- O modelo Random Forest captura não linearidades; o Linear Regression serve como base de comparação.\n")
        f.write("- As métricas MAE, RMSE e R² mostram precisão e capacidade explicativa.\n")

    logger.info(f"Modelos preditivos salvos em {model_dir}")
    logger.info(f"Previsões exportadas em {PREDICTION_EXPORT}")


if __name__ == "__main__":
    main()
