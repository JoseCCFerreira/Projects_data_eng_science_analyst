import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE = BASE_DIR / "config" / "settings.yml"
RAW_CSV = BASE_DIR / "data" / "raw" / "sensor_readings.csv"
SQLITE_DB = BASE_DIR / "data" / "transactional" / "transactional.db"
DUCKDB_FILE = BASE_DIR / "data" / "analytical" / "analytics.duckdb"
CLEAN_CSV = BASE_DIR / "data" / "processed" / "clean_sensor_readings.csv"
RESAMPLED_HOURLY = BASE_DIR / "data" / "processed" / "resampled_hourly.csv"
RESAMPLED_DAILY = BASE_DIR / "data" / "processed" / "resampled_daily.csv"
FILTERED_CSV = BASE_DIR / "data" / "processed" / "filtered_sensor_readings.csv"
CLUSTERING_EXPORT = BASE_DIR / "data" / "exports" / "clustering_results.csv"
PREDICTION_EXPORT = BASE_DIR / "data" / "exports" / "predictions.csv"
LOG_FILE = BASE_DIR / "logs" / "project.log"

SQLITE_SCHEMA = {
    "sensors": "sensor_id, sensor_name, sensor_type",
    "machines": "machine_id, machine_name, machine_type",
    "locations": "location_id, location_name",
    "machine_status": "status_id, machine_status, description"
}
