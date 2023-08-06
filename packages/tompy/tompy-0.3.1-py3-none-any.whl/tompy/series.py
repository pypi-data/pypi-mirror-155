from typing import Optional

import numpy as np
import pandas as pd

from tompy import vector

###############################################################################
# series
###############################################################################


def describe(s: pd.Series) -> pd.Series:
    return pd.Series(
        data=vector.describe(s.values),
        index=vector.describe_meta().keys(),
        dtype=np.float64,
    )


def shift(s: pd.Series, lag: int) -> pd.Series:
    if lag == 0:
        return s
    return pd.Series(
        data=vector.shift(s.values, lag), index=s.index, dtype=np.float64
    )


def rolling_sum(s: pd.Series, window: int) -> pd.Series:
    return pd.Series(
        data=vector.rolling_sum(s.values, window),
        index=s.index,
        dtype=np.float64,
    )


def rolling_mean(s: pd.Series, window: int) -> pd.Series:
    return pd.Series(
        data=vector.rolling_mean(s.values, window),
        index=s.index,
        dtype=np.float64,
    )


def rolling_std(s: pd.Series, window: int) -> pd.Series:
    return pd.Series(
        data=vector.rolling_std(s.values, window),
        index=s.index,
        dtype=np.float64,
    )


def rolling_var(s: pd.Series, window: int) -> pd.Series:
    return pd.Series(
        data=vector.rolling_var(s.values, window),
        index=s.index,
        dtype=np.float64,
    )


def rolling_min(s: pd.Series, window: int) -> pd.Series:
    return pd.Series(
        data=vector.rolling_min(s.values, window),
        index=s.index,
        dtype=np.float64,
    )


def rolling_max(s: pd.Series, window: int) -> pd.Series:
    return pd.Series(
        data=vector.rolling_max(s.values, window),
        index=s.index,
        dtype=np.float64,
    )


def rolling_corr(s1: pd.Series, s2: pd.Series, window: int) -> pd.Series:
    return s1.rolling(window).corr(s2, ddof=1)


def rolling_ema(s: pd.Series, window: int) -> pd.Series:
    return s.ewm(span=window, adjust=False).mean()


###############################################################################
# price
###############################################################################


def price2sr(price: pd.Series) -> pd.Series:
    return pd.Series(
        data=vector.price2sr(price.values), index=price.index, dtype=np.float64
    )


def price2lr(price: pd.Series) -> pd.Series:
    return pd.Series(
        data=vector.price2lr(price.values), index=price.index, dtype=np.float64
    )


def price_metrics(
    price: pd.Series,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.Series:
    return pd.Series(
        data=vector.price_metrics(
            price.values,
            ann_factor,
            sqrt_ann_factor,
            mode,
        ),
        index=vector.lr_sr_metrics_meta(mode).keys(),
        dtype=np.float64,
    )


def price_terms_metrics(
    price: pd.Series,
    terms: dict[str, int],
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.DataFrame:
    return pd.DataFrame(
        data=vector.price_terms_metrics(
            price.values,
            list(terms.values()),
            ann_factor,
            sqrt_ann_factor,
            mode,
        ),
        index=vector.lr_sr_metrics_meta(mode).keys(),
        columns=terms.keys(),
        dtype=np.float64,
    )


def price_dterms_metrics(price: pd.Series, mode: int = 0) -> pd.DataFrame:
    n = price.shape[0]
    ann_factor = 252
    D = 1
    W = 5
    M = 21
    Y = M * 12
    terms = {
        "1D": 1 * D,
        "1W": 1 * W,
        "2W": 2 * W,
        "1M": 1 * M,
        "3M": 3 * M,
        "6M": 6 * M,
        "1Y": 1 * Y,
        "3Y": 3 * Y,
        "5Y": 5 * Y,
        "10Y": 10 * Y,
        "ITD": n,
    }
    return price_terms_metrics(price, terms, ann_factor, mode=mode)


###############################################################################
# sr
###############################################################################


def sr2lr(sr: pd.Series) -> pd.Series:
    return pd.Series(
        data=vector.sr2lr(sr.values), index=sr.index, dtype=np.float64
    )


def sr_metrics(
    sr: pd.Series,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.Series:
    return pd.Series(
        data=vector.sr_metrics(sr.values, ann_factor, sqrt_ann_factor, mode),
        index=vector.lr_sr_metrics_meta(mode).keys(),
        dtype=np.float64,
    )


###############################################################################
# lr
###############################################################################


def lr2sr(lr: pd.Series) -> pd.Series:
    return pd.Series(
        data=vector.lr2sr(lr.values), index=lr.index, dtype=np.float64
    )


def lr2crdd(lr: pd.Series) -> pd.DataFrame:
    lr0_cr, lr0_dd = vector.lr2crdd(lr.values)
    return pd.DataFrame(
        data=np.asarray([lr0_cr, lr0_dd], dtype=np.float64).T,
        index=lr.index,
        columns=["LR_CR", "LR_DD"],
        dtype=np.float64,
    )


def lr_metrics(
    lr: pd.Series,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.Series:
    return pd.Series(
        data=vector.lr_metrics(lr.values, ann_factor, sqrt_ann_factor, mode),
        index=vector.lr_sr_metrics_meta(mode).keys(),
        dtype=np.float64,
    )


###############################################################################
# lr & sr
###############################################################################


def lr_sr_metrics(
    lr: pd.Series,
    sr: pd.Series,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> pd.Series:
    return pd.Series(
        data=vector.lr_sr_metrics(
            lr.values, sr.values, ann_factor, sqrt_ann_factor, mode
        ),
        index=vector.lr_sr_metrics_meta(mode).keys(),
        dtype=np.float64,
    )
