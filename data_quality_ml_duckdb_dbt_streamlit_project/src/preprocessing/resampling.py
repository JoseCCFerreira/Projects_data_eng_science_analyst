import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd
from src.utils.paths import CLEAN_CSV, RESAMPLED_HOURLY, RESAMPLED_DAILY
from src.utils.logging_config import logger


def main():
    df = pd.read_csv(CLEAN_CSV, parse_dates=["timestamp"], dayfirst=False)
    df = df.set_index("timestamp")
    numeric_cols = ["temperature", "humidity", "pressure", "vibration", "energy_consumption", "target_failure_risk"]

    hourly = df.groupby([pd.Grouper(freq="h"), "machine_id"])[numeric_cols].agg(["mean", "min", "max", "std", "count"])
    hourly.columns = ["_" .join(col).strip() for col in hourly.columns.values]
    hourly = hourly.reset_index()
    hourly.to_csv(RESAMPLED_HOURLY, index=False)

    daily = df.groupby([pd.Grouper(freq="D"), "machine_id"])[numeric_cols].agg(["mean", "min", "max", "std", "count"])
    daily.columns = ["_".join(col).strip() for col in daily.columns.values]
    daily = daily.reset_index()
    daily.to_csv(RESAMPLED_DAILY, index=False)

    logger.info(f"Resampling horário salvo em {RESAMPLED_HOURLY}")
    logger.info(f"Resampling diário salvo em {RESAMPLED_DAILY}")
    print(f"Resampled hourly: {RESAMPLED_HOURLY}")
    print(f"Resampled daily: {RESAMPLED_DAILY}")


if __name__ == "__main__":
    main()
