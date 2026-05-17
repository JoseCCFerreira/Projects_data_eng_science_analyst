import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd


def profile_statistics(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.select_dtypes(include=["number"])
    profile = numeric.agg(["count", "mean", "median", "std", "min", "max", "skew", "kurtosis"]).T
    profile = profile.reset_index().rename(columns={"index": "feature"})
    return profile


def correlation_matrix(df: pd.DataFrame):
    numeric = df.select_dtypes(include=["number"])
    return numeric.corr()
