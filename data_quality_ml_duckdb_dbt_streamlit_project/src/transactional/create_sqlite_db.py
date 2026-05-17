import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import sqlite3
from src.utils.paths import SQLITE_DB
from src.utils.logging_config import logger


def create_database():
    SQLITE_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS locations (location_id INTEGER PRIMARY KEY, location_name TEXT UNIQUE NOT NULL);"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS machines (machine_id INTEGER PRIMARY KEY, machine_name TEXT UNIQUE NOT NULL, machine_type TEXT);"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS sensors (sensor_id INTEGER PRIMARY KEY, sensor_name TEXT UNIQUE NOT NULL, sensor_type TEXT);"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS machine_status (status_id INTEGER PRIMARY KEY, machine_status TEXT UNIQUE NOT NULL, description TEXT);"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS sensor_readings ("
        "reading_id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "timestamp TEXT, "
        "sensor_id INTEGER, "
        "machine_id INTEGER, "
        "location_id INTEGER, "
        "temperature REAL, "
        "humidity REAL, "
        "pressure REAL, "
        "vibration REAL, "
        "energy_consumption REAL, "
        "status_id INTEGER, "
        "target_failure_risk REAL, "
        "FOREIGN KEY(sensor_id) REFERENCES sensors(sensor_id), "
        "FOREIGN KEY(machine_id) REFERENCES machines(machine_id), "
        "FOREIGN KEY(location_id) REFERENCES locations(location_id), "
        "FOREIGN KEY(status_id) REFERENCES machine_status(status_id)"
        ");"
    )
    conn.commit()
    conn.close()
    logger.info(f"SQLite database created em {SQLITE_DB}")


if __name__ == "__main__":
    create_database()
