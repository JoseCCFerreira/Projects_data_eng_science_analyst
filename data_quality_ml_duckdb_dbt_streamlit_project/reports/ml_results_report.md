# ML Results Report

## Clustering Evaluation
- kmeans: silhouette_score = 0.1994
- dbscan: silhouette_score = nan
- agglomerative: silhouette_score = 0.1307

## Observações
- KMeans identifica grupos por similaridade global.
- DBSCAN informa ruído e agrupamentos densos.
- Agglomerative destaca estruturas hierárquicas.
- PCA reduz para 2D e ajuda a interpretar agrupamentos.

## Predictive Modeling
### Linear Regression
- mae: 0.1015
- rmse: 0.1384
- r2: 0.6809
### Random Forest Regressor
- mae: 0.0983
- rmse: 0.1320
- r2: 0.7098

- O modelo Random Forest captura não linearidades; o Linear Regression serve como base de comparação.
- As métricas MAE, RMSE e R² mostram precisão e capacidade explicativa.
