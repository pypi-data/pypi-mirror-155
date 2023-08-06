from typing import Optional

import numpy as np
import pandas as pd

from tompy import matrix, series

###############################################################################
# dataFrame
###############################################################################


def drop_weekends(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.index.dayofweek < 5]


def read_csv(
    fpath: str, index_col: Optional[int] = 0, parse_dates: bool = True
) -> pd.DataFrame:
    return pd.read_csv(fpath, index_col=index_col, parse_dates=parse_dates)


def write_csv(df: pd.DataFrame, fpath: str) -> None:
    df.to_csv(fpath)


def describe(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.describe(df.values),
        index=matrix.describe_meta().keys(),
        columns=df.columns,
        dtype=np.float64,
    )


def shift(df: pd.DataFrame, lag: int) -> pd.DataFrame:
    if lag == 0:
        return df
    return pd.DataFrame(
        data=matrix.shift(df.values, lag),
        index=df.index,
        columns=df.columns,
        dtype=np.float64,
    )


def rolling_sum(df: pd.DataFrame, window: int) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.rolling_sum(df.values, window),
        index=df.index,
        columns=df.columns,
        dtype=np.float64,
    )


def rolling_mean(df: pd.DataFrame, window: int) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.rolling_mean(df.values, window),
        index=df.index,
        columns=df.columns,
        dtype=np.float64,
    )


def rolling_std(df: pd.DataFrame, window: int) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.rolling_std(df.values, window),
        index=df.index,
        columns=df.columns,
        dtype=np.float64,
    )


def rolling_var(df: pd.DataFrame, window: int) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.rolling_var(df.values, window),
        index=df.index,
        columns=df.columns,
        dtype=np.float64,
    )


def rolling_min(df: pd.DataFrame, window: int) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.rolling_min(df.values, window),
        index=df.index,
        columns=df.columns,
        dtype=np.float64,
    )


def rolling_max(df: pd.DataFrame, window: int) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.rolling_max(df.values, window),
        index=df.index,
        columns=df.columns,
        dtype=np.float64,
    )


def rolling_corr(df: pd.DataFrame, window: int, cidx: int = 0) -> pd.DataFrame:
    s = df[df.columns[cidx]]
    df2 = pd.DataFrame(index=df.index, columns=df.columns, dtype=np.float64)
    for col in df:
        df2[col] = series.rolling_corr(s, df[col], window)
    return df2


def rolling_ema(df: pd.DataFrame, window: int) -> pd.DataFrame:
    return df.ewm(span=window, adjust=False).mean()


###############################################################################
# price
###############################################################################


def price2sr(price: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.price2sr(price.values),
        index=price.index,
        columns=price.columns,
        dtype=np.float64,
    )


def price2lr(price: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.price2lr(price.values),
        index=price.index,
        columns=price.columns,
        dtype=np.float64,
    )


def price_metrics(
    price: pd.DataFrame,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.price_metrics(
            price.values, ann_factor, sqrt_ann_factor, mode
        ),
        index=matrix.lr_sr_metrics_meta(mode).keys(),
        columns=price.columns,
        dtype=np.float64,
    )


###############################################################################
# sr
###############################################################################


def sr2lr(sr: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.sr2lr(sr.values),
        index=sr.index,
        columns=sr.columns,
        dtype=np.float64,
    )


def sr_metrics(
    sr: pd.DataFrame,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.sr_metrics(sr.values, ann_factor, sqrt_ann_factor, mode),
        index=matrix.lr_sr_metrics_meta(mode).keys(),
        columns=sr.columns,
        dtype=np.float64,
    )


###############################################################################
# lr
###############################################################################


def lr2sr(lr: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.lr2sr(lr.values),
        index=lr.index,
        columns=lr.columns,
        dtype=np.float64,
    )


def lr2crdd(lr: pd.DataFrame) -> dict[str, pd.DataFrame]:
    lr0_cr, lr0_dd = matrix.lr2crdd(lr.values)
    return {
        "LR_CR": pd.DataFrame(
            data=lr0_cr, index=lr.index, columns=lr.columns, dtype=np.float64
        ),
        "LR_DD": pd.DataFrame(
            data=lr0_dd, index=lr.index, columns=lr.columns, dtype=np.float64
        ),
    }


def lr_metrics(
    lr: pd.DataFrame,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.lr_metrics(lr.values, ann_factor, sqrt_ann_factor, mode),
        index=matrix.lr_sr_metrics_meta(mode).keys(),
        columns=lr.columns,
        dtype=np.float64,
    )


###############################################################################
# lr & sr
###############################################################################


def lr_sr_metrics(
    lr: pd.DataFrame,
    sr: pd.DataFrame,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.DataFrame:
    return pd.DataFrame(
        data=matrix.lr_sr_metrics(
            lr.values, sr.values, ann_factor, sqrt_ann_factor, mode
        ),
        index=matrix.lr_sr_metrics_meta(mode).keys(),
        columns=lr.columns,
        dtype=np.float64,
    )


###############################################################################
# portfolio
###############################################################################


def portfolio_price(
    price: pd.DataFrame,
    weights: pd.DataFrame,
    fee_rate: float,
) -> pd.Series:
    price = price[weights.columns]
    price = price.loc[weights.index]
    return pd.Series(
        data=matrix.portfolio_price(price.values, weights.values, fee_rate),
        index=price.index,
        dtype=np.float64,
    )
