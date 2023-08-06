import pandas as pd
import numpy as np
from slugify import slugify
from munch import Munch as Dict
from . import xsettings, xpd


def drop_na_cols_df(df):
    if len(df) == 0:
        return df

    df = df.copy()
    for col_name in df.columns:
        sa = df[col_name]

        if not pd.api.types.is_numeric_dtype(sa):
            continue

        if np.isnan(sa).sum() == len(sa):
            del df[col_name]

    return df


def read_csv(csv_path, na_values=None, low_memory=False, drop_na_cols=True, skiprows=None, skipfooter=0):
    """
    A simple wrapper for read_csv that cleans it up a bit in the process..
    """
    na_values = xsettings.get_default(xsettings.NAN_TEXTS, na_values)

    engine = 'python' if skipfooter else 'c'

    df = pd.read_csv(csv_path, keep_default_na=False, na_values=na_values, low_memory=low_memory, skiprows=skiprows, skipfooter=skipfooter, engine=engine)
    xpd.x_clean_column_names(df, inplace=True)

    if drop_na_cols:
        df = drop_na_cols_df(df)

    return df


def read_excel(excel_path, na_values=None, drop_na_cols=True):
    """
    A simple wrapper for read_excel that cleans it up a bit in the process,
      as well as returns a different dataframe for each sheet
    """
    na_values = xsettings.get_default(xsettings.NAN_TEXTS, na_values)

    res = pd.read_excel(excel_path, sheet_name=None, na_values=na_values)

    res_new = Dict()
    for k in list(res.keys()):
        k_new = slugify(k, separator='_')
        df = res[k]
        xpd.x_clean_column_names(df, inplace=True)
        if drop_na_cols:
            df = drop_na_cols_df(df)

        assert k_new not in res_new, k_new
        res_new[k_new] = df

    return res_new


def filter_all_on(*args, on=None):
    """
    Given two or more dataframes, returns them filtered as if they went through an inner-join
    """

    assert on, "must provide 'on' parameter"
    if len(args) < 2:
        return args

    set_all = args[0][on].unique()
    for df in args[1:]:
        set_curr = df[on].unique()
        set_all = np.intersect1d(set_all, set_curr)

    filtered = []
    for df in args:
        df = df[df[on].isin(set_all)]
        filtered.append(df)

    return tuple(filtered)

