# How to Run

1. Crie e ative um ambiente virtual Python.
2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Gere os dados:

```bash
make generate-data
```

4. Crie a base SQLite e carregue os dados:

```bash
make load-sqlite
```

5. Crie a base DuckDB:

```bash
make load-duckdb
```

6. Rode dbt:

```bash
make dbt-run
make dbt-test
```

7. Gere o relatório de qualidade:

```bash
make quality-report
```

8. Limpe, reamostre e filtre:

```bash
make clean-data
make resample
make filter-noise
```

9. Treine ML:

```bash
make train-clustering
make train-prediction
```

10. Abra o Streamlit:

```bash
make streamlit
```
