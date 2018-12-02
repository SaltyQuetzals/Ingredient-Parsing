"""Evaluates results of CRF provided by NYT"""
import json

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

EVAL_COLS = ["name", "qty", "range_end", "unit", "comment"]
COL_NAMES = EVAL_COLS + ["input"]


def build_csv(filename: str) -> pd.DataFrame:
    """Given the output of the NYT's CRF, converts it to a Pandas DataFrame.

    Args:
        filename: The name of the file to open
    """
    cols = {key: [] for key in COL_NAMES}
    with open(filename, "r") as file_pointer:
        json_data = json.load(file_pointer)
        for item in json_data:
            for key in COL_NAMES:
                val = item.get(key, np.nan)
                if val:
                    cols[key].append(val)
                else:
                    if key in ('qty', 'range_end'):
                        cols[key].append(0.0)
                    else:
                        cols[key].append(val)
    return pd.DataFrame(data=cols)


def main():
    """Evaluates results of CRF provided by NYT"""
    predicted_df = build_csv("../results.json")

    predicted_df.to_csv('predicted.csv', index=False)


if __name__ == "__main__":
    main()
