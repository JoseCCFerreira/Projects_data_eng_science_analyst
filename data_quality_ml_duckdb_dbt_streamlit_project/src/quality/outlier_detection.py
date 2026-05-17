import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd


def detect_iqr_outliers(df: pd.DataFrame, features):
    records = []
    for col in features:
        if pd.api.types.is_numeric_dtype(df[col]):
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            mask = (df[col] < lower) | (df[col] > upper)
            records.append({
                "feature": col,
                "outliers": int(mask.sum()),
                "outlier_ratio": float(mask.mean()),
                "lower_bound": lower,
                "upper_bound": upper,
            })
    return pd.DataFrame(records)


def zscore_filter(df: pd.DataFrame, features, threshold=3.0):
    result = df.copy()
    for col in features:
        if pd.api.types.is_numeric_dtype(result[col]):
            z = (result[col] - result[col].mean()) / result[col].std(ddof=0)
            result = result[abs(z) <= threshold]
    return result
