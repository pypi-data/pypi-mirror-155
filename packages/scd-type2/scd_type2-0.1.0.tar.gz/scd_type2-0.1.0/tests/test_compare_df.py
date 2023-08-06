from datetime import date

import pandas as pd
from pandas.testing import assert_frame_equal

from scd_type2.compare import compare_dfs

today = date.today().strftime("%d/%m/%Y")


def test_compare_dfs():
    df1 = pd.DataFrame({'A': [1, 2, 3, 3],
                        'B': [2, 3, 4, 4]})

    df2 = pd.DataFrame({'A': [1], 'B': [2]})

    response_start_df = pd.DataFrame.from_dict({'A': {0: 2, 1: 3, 2: 1},
                                                'B': {0: 3, 1: 4, 2: 2},
                                                'active': {0: 1, 1: 1, 2: 1},
                                                'start_date': {0: today, 1: today, 2: today}})
    response_end_df = pd.DataFrame.from_dict({'A': {0: 1}, 'B': {0: 2}, 'active': {0: 0}, 'end_date': {0: today}})

    idx = "A"
    start, end = compare_dfs(df1, df2, idx)
    assert_frame_equal(start, response_start_df)
    assert_frame_equal(end, response_end_df)

    idx = ["A"]
    start, end = compare_dfs(df1, df2, idx)
    assert_frame_equal(start, response_start_df)
    assert_frame_equal(end, response_end_df)

    idx = ["A", "B"]
    start, end = compare_dfs(df1, df2, idx)
    assert_frame_equal(start, response_start_df)
    assert_frame_equal(end, response_end_df)
