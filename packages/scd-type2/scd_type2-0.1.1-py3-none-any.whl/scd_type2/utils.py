import warnings

import pandas as pd

from scd_type2.config import COLOURS, today


def duplicate_warn():
    warnings.warn(
        f"\n{COLOURS['RED']}Warning:{COLOURS['EOC']} There are multiple common records in DataFrame based on index.\n")


def make_expired(df: pd.DataFrame):
    if len(df) == 0:
        df = None
    else:
        df["active"] = 0
        df["end_date"] = today
    return df


def make_new(df: pd.DataFrame):
    if len(df) == 0:
        df = None
    else:
        df["active"] = 1
        df["start_date"] = today
    return df
