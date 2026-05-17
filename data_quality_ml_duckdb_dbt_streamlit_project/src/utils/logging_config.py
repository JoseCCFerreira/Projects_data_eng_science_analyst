import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import logging
from pathlib import Path

LOG_FOLDER = Path(__file__).resolve().parents[2] / "logs"
LOG_FOLDER.mkdir(exist_ok=True)
LOG_FILE = LOG_FOLDER / "project.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("data_quality_ml")
