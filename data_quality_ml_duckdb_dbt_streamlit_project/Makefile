PYTHON=python3
PROJECT_DIR=$(CURDIR)

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

generate-data:
	$(PYTHON) src/ingest/create_synthetic_dataset.py

load-sqlite:
	$(PYTHON) src/transactional/create_sqlite_db.py
	$(PYTHON) src/transactional/load_to_sqlite.py

load-duckdb:
	$(PYTHON) src/analytical/create_duckdb.py
	$(PYTHON) src/analytical/load_to_duckdb.py

dbt-run:
	cd dbt_project && dbt run

dbt-test:
	cd dbt_project && dbt test

quality-report:
	$(PYTHON) src/quality/data_quality_report.py

clean-data:
	$(PYTHON) src/preprocessing/cleaning.py

resample:
	$(PYTHON) src/preprocessing/resampling.py

filter-noise:
	$(PYTHON) src/preprocessing/noise_filtering.py

train-clustering:
	$(PYTHON) src/ml/clustering.py

train-prediction:
	$(PYTHON) src/ml/prediction.py

streamlit:
	streamlit run streamlit_app/app.py

all: setup generate-data load-sqlite load-duckdb dbt-run quality-report clean-data resample filter-noise train-clustering train-prediction
