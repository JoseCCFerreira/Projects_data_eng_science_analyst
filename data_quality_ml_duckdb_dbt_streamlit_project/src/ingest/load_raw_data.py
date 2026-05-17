import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd
from pathlib import Path
from src.utils.paths import RAW_CSV
from src.utils.logging_config import logger


def main():
    if not RAW_CSV.exists():
        logger.error(f"Ficheiro não encontrado: {RAW_CSV}")
        raise FileNotFoundError(f"Ficheiro não encontrado: {RAW_CSV}")

    df = pd.read_csv(RAW_CSV, parse_dates=["timestamp"], dayfirst=False)
    logger.info(f"Carregado raw file: {RAW_CSV}")
    logger.info(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")
    logger.info(f"Tipos de dados:\n{df.dtypes}")
    print("--- Raw data summary ---")
    print(f"Path: {RAW_CSV}")
    print(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")
    print(df.dtypes)

    return df


if __name__ == "__main__":
    main()
