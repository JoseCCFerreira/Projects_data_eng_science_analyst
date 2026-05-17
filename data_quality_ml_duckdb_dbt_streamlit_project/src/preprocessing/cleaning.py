import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd
from src.utils.paths import RAW_CSV, CLEAN_CSV
from src.utils.logging_config import logger


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["machine_status"] = df["machine_status"].astype(str).str.lower().str.strip()
    df["machine_status"] = df["machine_status"].replace({
        "running": "running",
        "idle": "idle",
        "maintenance": "maintenance",
        "fault": "fault",
        "unknown": "unknown",
    })
    df["location"] = df["location"].astype(str).str.strip().replace({"East Plant ": "East Plant", "West Plant ": "West Plant"})
    df["sensor_id"] = df["sensor_id"].astype(str)
    df["machine_id"] = df["machine_id"].astype(str)
    df = df.drop_duplicates()
    df = df[df["timestamp"].notna()]
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df[df["timestamp"].notna()]
    numeric_cols = ["temperature", "humidity", "pressure", "vibration", "energy_consumption", "target_failure_risk"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[df["temperature"] < -20, "temperature"] = df["temperature"].median()
    df.loc[df["temperature"] > 120, "temperature"] = df["temperature"].median()
    df.loc[df["humidity"] < 0, "humidity"] = df["humidity"].median()
    df.loc[df["humidity"] > 100, "humidity"] = df["humidity"].median()
    df.loc[df["pressure"] < 80, "pressure"] = df["pressure"].median()
    df.loc[df["pressure"] > 120, "pressure"] = df["pressure"].median()
    df["vibration"] = df["vibration"].clip(lower=0)
    df["target_failure_risk"] = df["target_failure_risk"].clip(0, 1)
    df = df.ffill().bfill()
    return df


def main():
    df = pd.read_csv(RAW_CSV, parse_dates=["timestamp"], dayfirst=False)
    clean_df = clean_data(df)
    CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(CLEAN_CSV, index=False)
    logger.info(f"Dados limpos gravados em {CLEAN_CSV} com {len(clean_df)} linhas")
    print(f"Dados limpos gravados em {CLEAN_CSV}")


if __name__ == "__main__":
    main()
