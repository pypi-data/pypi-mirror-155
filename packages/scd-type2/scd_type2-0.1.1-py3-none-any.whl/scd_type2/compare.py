#! /usr/bin/env python3

"""
Script to compare source data with target data and get new DataFrame to be uploaded
to database, flagged as whether new (active=1) or old (active=0).
"""

from typing import Union

import pandas as pd

from scd_type2.utils import duplicate_warn, make_expired, make_new


def compare_dfs(df1: pd.DataFrame, df2: pd.DataFrame, idx: Union[list, str] = None):
    """
    Returns one DataFrame of rows to be created and one DataFrame of rows to be updated
    logic:
        if row of df1[idx] exists in df2[idx], then add to df1 row to create DataFrame and add df2 row to update
            DataFrame, with status inactive
        if row of df1[idx] does not exist in df2[idx], then add to create DataFrame
        otherwise, no action
    """
    # We only care about rows with at least one difference
    if idx is not None:
        df_all = df1.merge(df2.drop_duplicates(), how='left', indicator=True)
        df1 = df_all[df_all['_merge'] == 'left_only']

    if isinstance(idx, str):
        idx = [idx]
    elif idx is None:
        # All columns of both, which must be the same
        idx = df1.columns.to_list()

    sub_df1 = df1[idx]
    sub_df2 = df2[idx]

    # Duplicates removed, but may cause unexpected results
    if len(sub_df1) != len(sub_df1.drop_duplicates()):
        duplicate_warn()
        sub_df1.drop_duplicates(inplace=True)

    if len(sub_df2) != len(sub_df2.drop_duplicates()):
        duplicate_warn()
        sub_df2.drop_duplicates(inplace=True)

    merge_df = sub_df1.merge(sub_df2, indicator=True, how='left')
    end_idx = merge_df.copy(deep=True).loc[lambda x: x['_merge'] == 'both'].index

    end_df_old = df1.loc[end_idx]
    end_df = make_expired(end_df_old)

    end_df_new = df2.loc[end_idx]
    end_df_new = make_new(end_df_new)

    start_idx = merge_df.copy(deep=True).loc[lambda x: x['_merge'] == 'left_only'].index
    start_df = df1.loc[start_idx]
    start_df = make_new(start_df)

    start_df = pd.concat([start_df, end_df_new], ignore_index=True)

    return start_df, end_df
