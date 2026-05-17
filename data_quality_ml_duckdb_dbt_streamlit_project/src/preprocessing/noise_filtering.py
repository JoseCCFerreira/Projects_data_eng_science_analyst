import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd
from scipy.signal import savgol_filter
from src.utils.paths import CLEAN_CSV, FILTERED_CSV
from src.utils.logging_config import logger


def noise_filter(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["machine_id", "sensor_id", "timestamp"])
    df["temperature_ma"] = df.groupby(["machine_id", "sensor_id"])["temperature"].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
    df["humidity_med"] = df.groupby(["machine_id", "sensor_id"])["humidity"].transform(lambda x: x.rolling(window=5, min_periods=1).median())
    for col in ["pressure", "vibration", "energy_consumption"]:
        df[f"{col}_zscore"] = df.groupby(["machine_id", "sensor_id"])[col].transform(lambda x: (x - x.mean()) / x.std(ddof=0))
    df = df[(df[["pressure_zscore", "vibration_zscore", "energy_consumption_zscore"]].abs() <= 3).all(axis=1)]
    def smooth_temp(x):
        y = x.ffill().bfill()
        if len(y) < 5:
            return y
        window = 5 if len(y) >= 5 else len(y) if len(y) % 2 == 1 else len(y) - 1
        if window < 3:
            return y
        return pd.Series(savgol_filter(y, window, 2), index=x.index)

    df["temperature_savgol"] = df.groupby(["machine_id", "sensor_id"])["temperature"].transform(smooth_temp)
    df = df.drop(columns=["pressure_zscore", "vibration_zscore", "energy_consumption_zscore"])
    return df


def main():
    df = pd.read_csv(CLEAN_CSV, parse_dates=["timestamp"], dayfirst=False)
    filtered = noise_filter(df)
    FILTERED_CSV.parent.mkdir(parents=True, exist_ok=True)
    filtered.to_csv(FILTERED_CSV, index=False)
    logger.info(f"Dados filtrados salvos em {FILTERED_CSV}")
    print(f"Filtered dataset: {FILTERED_CSV}")


if __name__ == "__main__":
    main()
