import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import sqlite3
import pandas as pd
from src.utils.paths import SQLITE_DB, RAW_CSV
from src.utils.logging_config import logger

STATUS_MAP = {
    "running": "Operational",
    "idle": "Idle",
    "maintenance": "Maintenance",
    "fault": "Fault",
    "RUNNING": "Operational",
    "IDLE": "Idle",
    "MAINTENANCE": "Maintenance",
    "FAULT": "Fault",
}


def normalize_source(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["machine_status"] = df["machine_status"].astype(str).str.lower().map(STATUS_MAP).fillna("Unknown")
    df["location"] = df["location"].astype(str).str.strip().replace({"East Plant ": "East Plant", "West Plant ": "West Plant"})
    df["machine_id"] = df["machine_id"].astype(str)
    df["sensor_id"] = df["sensor_id"].astype(str)
    return df


def load_data():
    if not RAW_CSV.exists():
        logger.error(f"Raw file não existe: {RAW_CSV}")
        raise FileNotFoundError(RAW_CSV)

    df = pd.read_csv(RAW_CSV, parse_dates=["timestamp"], dayfirst=False)
    df = normalize_source(df)

    with sqlite3.connect(SQLITE_DB) as conn:
        cursor = conn.cursor()
        locations = df["location"].dropna().unique().tolist()
        cursor.executemany("INSERT OR IGNORE INTO locations(location_name) VALUES (?);", [(loc,) for loc in locations])

        machines = df["machine_id"].dropna().unique().tolist()
        cursor.executemany(
            "INSERT OR IGNORE INTO machines(machine_name, machine_type) VALUES (?, ?);",
            [(machine, "industrial") for machine in machines],
        )

        sensors = df["sensor_id"].dropna().unique().tolist()
        cursor.executemany(
            "INSERT OR IGNORE INTO sensors(sensor_name, sensor_type) VALUES (?, ?);",
            [(sensor, "industrial") for sensor in sensors],
        )

        statuses = [(status, status) for status in set(df["machine_status"].dropna().unique().tolist())]
        cursor.executemany("INSERT OR IGNORE INTO machine_status(machine_status, description) VALUES (?, ?);", statuses)
        conn.commit()

        location_map = {row[1]: row[0] for row in cursor.execute("SELECT location_id, location_name FROM locations").fetchall()}
        machine_map = {row[1]: row[0] for row in cursor.execute("SELECT machine_id, machine_name FROM machines").fetchall()}
        sensor_map = {row[1]: row[0] for row in cursor.execute("SELECT sensor_id, sensor_name FROM sensors").fetchall()}
        status_map = {row[1]: row[0] for row in cursor.execute("SELECT status_id, machine_status FROM machine_status").fetchall()}

        insert_rows = []
        for _, row in df.iterrows():
            insert_rows.append(
                (
                    row["timestamp"].isoformat() if pd.notna(row["timestamp"]) else None,
                    sensor_map.get(row["sensor_id"]),
                    machine_map.get(row["machine_id"]),
                    location_map.get(row["location"]),
                    row["temperature"],
                    row["humidity"],
                    row["pressure"],
                    row["vibration"],
                    row["energy_consumption"],
                    status_map.get(row["machine_status"]),
                    row["target_failure_risk"],
                )
            )

        cursor.executemany(
            "INSERT INTO sensor_readings(timestamp, sensor_id, machine_id, location_id, temperature, humidity, pressure, vibration, energy_consumption, status_id, target_failure_risk) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            insert_rows,
        )
        conn.commit()

    logger.info(f"Dados carregados em SQLite: {SQLITE_DB} com {len(insert_rows)} leituras")


if __name__ == "__main__":
    load_data()
