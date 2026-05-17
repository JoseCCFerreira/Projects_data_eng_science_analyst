import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import random
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from datetime import timedelta
from src.utils.paths import RAW_CSV
from src.utils.logging_config import logger


def load_settings():
    config_path = Path(__file__).resolve().parents[2] / "config" / "settings.yml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def create_timestamps(start_date, end_date, irregularity_rate=0.08):
    timestamps = pd.date_range(start=start_date, end=end_date, freq="h").to_pydatetime().tolist()
    if irregularity_rate > 0:
        drop_count = int(len(timestamps) * irregularity_rate)
        np.random.seed(42)
        drop_ids = np.random.choice(len(timestamps), size=drop_count, replace=False)
        timestamps = [ts for idx, ts in enumerate(timestamps) if idx not in drop_ids]
    return timestamps


def make_sensor_data(settings):
    np.random.seed(0)
    sensors = [f"sensor_{i+1}" for i in range(settings["parameters"]["n_sensors"])]
    machines = [f"machine_{i+1}" for i in range(settings["parameters"]["n_machines"])]
    locations = settings["parameters"]["locations"]

    timestamps = create_timestamps(
        settings["parameters"]["start_date"],
        settings["parameters"]["end_date"],
        settings["parameters"]["irregularity_rate"],
    )

    records = []
    for ts in timestamps:
        for sensor in sensors:
            machine = random.choice(machines)
            location = random.choice(locations)
            base_temp = 60 + 10 * machines.index(machine)
            temperature = np.random.normal(loc=base_temp, scale=5)
            humidity = np.random.normal(loc=40 + 2 * locations.index(location), scale=8)
            pressure = np.random.normal(loc=101.3, scale=0.8)
            vibration = abs(np.random.normal(loc=1.2, scale=0.6))
            energy_consumption = np.random.normal(loc=120 + 15 * machines.index(machine), scale=20)
            failure_risk = min(max(np.random.beta(2, 8) + 0.02 * (temperature - 70), 0), 1)
            machine_status = random.choice(["running", "idle", "maintenance", "fault"])
            records.append({
                "timestamp": ts,
                "sensor_id": sensor,
                "machine_id": machine,
                "location": location,
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "pressure": round(pressure, 2),
                "vibration": round(vibration, 3),
                "energy_consumption": round(abs(energy_consumption), 2),
                "machine_status": machine_status,
                "target_failure_risk": round(failure_risk, 4),
            })

    df = pd.DataFrame(records)
    df = inject_quality_issues(df, settings)
    return df


def inject_quality_issues(df: pd.DataFrame, settings: dict) -> pd.DataFrame:
    n = len(df)
    np.random.seed(1)

    # Missing values
    missing_rows = np.random.choice(n, size=int(n * settings["parameters"]["missing_rate"]), replace=False)
    for col in ["temperature", "humidity", "pressure", "vibration"]:
        df.loc[missing_rows, col] = np.nan

    # Duplicates
    duplicate_rows = df.sample(frac=settings["parameters"]["duplicate_rate"], random_state=2)
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # Outliers and impossible values
    outlier_rows = np.random.choice(df.index, size=int(n * settings["parameters"]["outlier_rate"]), replace=False)
    df.loc[outlier_rows, "temperature"] *= np.where(np.random.rand(len(outlier_rows)) > 0.5, 1.8, -1.2)
    df.loc[outlier_rows, "humidity"] = df.loc[outlier_rows, "humidity"] * 2
    df.loc[outlier_rows, "pressure"] = df.loc[outlier_rows, "pressure"] + np.random.choice([20, -30], size=len(outlier_rows))
    df.loc[outlier_rows, "energy_consumption"] = df.loc[outlier_rows, "energy_consumption"] * 3

    # Categorical inconsistencies
    df.loc[df.sample(frac=0.03, random_state=3).index, "machine_status"] = df.loc[df.sample(frac=0.03, random_state=3).index, "machine_status"].str.upper()
    df.loc[df.sample(frac=0.02, random_state=4).index, "location"] = df.loc[df.sample(frac=0.02, random_state=4).index, "location"].str.replace("Plant", "Plant ")

    # Impossible sensor IDs and timestamps irregularities
    df.loc[df.sample(frac=0.01, random_state=5).index, "sensor_id"] = "sensor_999"
    df.loc[df.sample(frac=0.005, random_state=6).index, "timestamp"] = pd.NaT

    df = df.sample(frac=1, random_state=7).reset_index(drop=True)
    return df


def main():
    settings = load_settings()
    RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
    df = make_sensor_data(settings)
    df.to_csv(RAW_CSV, index=False)
    logger.info(f"Raw dataset gerado em {RAW_CSV} com {len(df)} linhas e {len(df.columns)} colunas")


if __name__ == "__main__":
    main()
