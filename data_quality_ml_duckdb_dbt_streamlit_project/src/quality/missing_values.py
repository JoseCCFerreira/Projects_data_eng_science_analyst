import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd


def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    result = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_ratio": df.isna().mean(),
    })
    result = result.reset_index().rename(columns={"index": "feature"})
    return result
