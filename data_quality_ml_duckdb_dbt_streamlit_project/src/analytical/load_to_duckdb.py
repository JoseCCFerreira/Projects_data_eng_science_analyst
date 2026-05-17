import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import duckdb
import sqlite3
import pandas as pd
from src.utils.paths import DUCKDB_FILE, SQLITE_DB
from src.utils.logging_config import logger


def load_duckdb():
    if not SQLITE_DB.exists():
        logger.error(f"SQLite DB não encontrado: {SQLITE_DB}")
        raise FileNotFoundError(SQLITE_DB)

    con = duckdb.connect(database=str(DUCKDB_FILE), read_only=False)
    sqlite_con = sqlite3.connect(SQLITE_DB)

    tables = ["locations", "machines", "sensors", "machine_status", "sensor_readings"]
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table};", sqlite_con)
        con.register(table, df)
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM {table};")

    con.close()
    sqlite_con.close()
    logger.info(f"Dados carregados de SQLite para DuckDB em {DUCKDB_FILE}")


if __name__ == "__main__":
    load_duckdb()
