import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import duckdb
from src.utils.paths import DUCKDB_FILE
from src.utils.logging_config import logger


def create_duckdb():
    DUCKDB_FILE.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(database=str(DUCKDB_FILE), read_only=False)
    con.execute("PRAGMA threads=4;")
    con.close()
    logger.info(f"DuckDB analítico criado em {DUCKDB_FILE}")


if __name__ == "__main__":
    create_duckdb()
