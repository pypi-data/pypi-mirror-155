from __future__ import annotations

import pandas as pd

from urtools.dict_tools.dict_nans import filter_dict_nans

def df_to_jsonlist(df: pd.DataFrame) -> list[dict]:
    return [filter_dict_nans(record) for record in df.to_dict(orient='records')]

def find_duplicates(df: pd.DataFrame, subset: str | list[str] | None = None) -> list[int]:
    df_post_drop = df.drop_duplicates(subset=subset)
    dropped_inds = sorted(set(df.index.tolist()).difference(df_post_drop.index.tolist()))
    return dropped_inds

def count_duplicates(df: pd.DataFrame, subset: str | list[str] | None = None) -> int:
    return len(find_duplicates(df, subset))
