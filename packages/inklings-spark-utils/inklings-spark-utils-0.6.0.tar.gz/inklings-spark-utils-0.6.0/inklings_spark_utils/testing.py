from pyspark.sql import Row
from itertools import zip_longest


class SchemasNotEqualError(Exception):
    """The schemas are not equal"""

    pass


class DataFramesNotEqualError(Exception):
    """The DataFrames are not equal"""

    pass


def assert_schema_equality(s1, s2):
    if s1 != s2:
        raise SchemasNotEqualError(
            "\n" + "Base:" + s1.fields + "\nCompare:" + s2.fields
        )


def assert_generic_rows_equality(df1, df2):
    df1_rows = df1.collect()
    df2_rows = df2.collect()
    zipped = list(zip_longest(df1_rows, df2_rows))
    allRowsEqual = True
    for r1, r2 in zipped:
        if (r1 is not None and r2 is None) or (r2 is not None and r1 is None):
            allRowsEqual = False
        if not are_rows_approx_equal(r1, r2):
            allRowsEqual = False
    if allRowsEqual == False:
        raise DataFramesNotEqualError("\n")


def are_rows_approx_equal(r1: Row, r2: Row, precision: float = 0.01) -> bool:
    d1 = r1.asDict()
    d2 = r2.asDict()
    allEqual = True
    for key in d1.keys() & d2.keys():
        if isinstance(d1[key], float) and isinstance(d2[key], float):
            if abs(d1[key] - d2[key]) > precision:
                allEqual = False
        elif d1[key] != d2[key]:
            allEqual = False
    return allEqual


def assert_approx_df_equality(df1, df2):
    assert_schema_equality(df1.schema, df2.schema)
    assert_generic_rows_equality(df1, df2)


def are_dfs_approx_equal(df1, df2):
    try:
        assert_approx_df_equality(df1, df2)
        return True
    except:
        pass


def are_dfs_equal(df1, df2):
    if df1.schema != df2.schema:
        return False
    if df1.collect() != df2.collect():
        return False
    return True
