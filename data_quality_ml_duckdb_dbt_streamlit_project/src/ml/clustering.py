import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from src.utils.paths import CLEAN_CSV, CLUSTERING_EXPORT
from src.utils.logging_config import logger
from pathlib import Path


def build_features(df: pd.DataFrame):
    features = ["temperature", "humidity", "pressure", "vibration", "energy_consumption", "target_failure_risk"]
    X = df[features].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X, X_scaled, scaler


def fit_models(X_scaled):
    models = {
        "kmeans": KMeans(n_clusters=4, random_state=42),
        "dbscan": DBSCAN(eps=1.5, min_samples=8),
        "agglomerative": AgglomerativeClustering(n_clusters=4),
    }
    results = {}
    for name, model in models.items():
        labels = model.fit_predict(X_scaled)
        results[name] = {"model": model, "labels": labels}
    return results


def evaluate_clusters(X_scaled, results):
    from sklearn.metrics import silhouette_score
    evaluation = {}
    for name, data in results.items():
        labels = data["labels"]
        if len(set(labels)) > 1 and -1 not in set(labels):
            score = silhouette_score(X_scaled, labels)
        else:
            score = float("nan")
        evaluation[name] = score
    return evaluation


def main():
    df = pd.read_csv(CLEAN_CSV, parse_dates=["timestamp"], dayfirst=False)
    X, X_scaled, scaler = build_features(df)
    results = fit_models(X_scaled)
    evaluation = evaluate_clusters(X_scaled, results)

    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(X_scaled)
    export_df = X.reset_index(drop=True).copy()
    export_df[["pca_1", "pca_2"]] = components
    for name, data in results.items():
        export_df[f"cluster_{name}"] = data["labels"]

    CLUSTERING_EXPORT.parent.mkdir(parents=True, exist_ok=True)
    export_df.to_csv(CLUSTERING_EXPORT, index=False)

    model_dir = Path(__file__).resolve().parents[2] / "models" / "clustering"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, model_dir / "scaler.joblib")
    joblib.dump(pca, model_dir / "pca.joblib")
    for name, data in results.items():
        joblib.dump(data["model"], model_dir / f"{name}.joblib")

    report_path = Path(__file__).resolve().parents[2] / "reports" / "ml_results_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        f.write("# ML Results Report\n\n")
        f.write("## Clustering Evaluation\n")
        for name, score in evaluation.items():
            f.write(f"- {name}: silhouette_score = {score:.4f}\n")
        f.write("\n## Observações\n")
        f.write("- KMeans identifica grupos por similaridade global.\n")
        f.write("- DBSCAN informa ruído e agrupamentos densos.\n")
        f.write("- Agglomerative destaca estruturas hierárquicas.\n")
        f.write("- PCA reduz para 2D e ajuda a interpretar agrupamentos.\n")

    logger.info(f"Clustering executado e resultados salvos em {CLUSTERING_EXPORT}")
    logger.info(f"Modelos salvos em {model_dir}")
    logger.info(f"Relatório de ML atualizado em {report_path}")


if __name__ == "__main__":
    main()
