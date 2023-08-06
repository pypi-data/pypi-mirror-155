from typing import Callable, Optional

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.optimize import minimize
from scipy.stats import kurtosis, skew

from tompy import anys, scalar

###############################################################################
# vector
###############################################################################


def validate(v: np.ndarray) -> int:
    assert v.ndim == 1
    return v.shape[0]


def validate_rolling(v: np.ndarray, window: int) -> int:
    assert window >= 0
    return validate(v)


def zeros(n: int) -> np.ndarray:
    return np.zeros(n, dtype=np.float64)


def nans(n: int) -> np.ndarray:
    return np.full(n, np.nan, dtype=np.float64)


def describe_meta() -> dict[str, str]:
    return {
        "COUNT": "Count",
        "MEAN": "Mean",
        "STD": "Standard Deviation",
        "SKEW": "Skewness",
        "KURT": "Kurtosis",
        "MIN": "Min",
        "25%": "25%",
        "50%": "50%",
        "75%": "75%",
        "MAX": "Max",
    }


def describe(v: np.ndarray) -> np.ndarray:
    n = validate(v)
    if n <= 0:
        return nans(len(describe_meta()))
    return np.asarray(
        [
            nancnt(v),
            nanmean(v),
            nanstd(v),
            nanskew(v),
            nankurt(v),
            nanpctl(v, 0),
            nanpctl(v, 25),
            nanpctl(v, 50),
            nanpctl(v, 75),
            nanpctl(v, 100),
        ],
        dtype=np.float64,
    )


def shift(v: np.ndarray, lag: int) -> np.ndarray:
    n = validate(v)
    if n <= 0 or lag == 0:
        return v
    if lag > 0:
        if lag >= n:
            return nans(n)
        return np.concatenate((nans(lag), v[:-lag]))
    lag = -lag
    if lag >= n:
        return nans(n)
    return np.concatenate((v[lag:], nans(lag)))


def nancnt(v: np.ndarray) -> int:
    n = validate(v)
    if n <= 0:
        return np.nan
    return n - anys.nansum(np.isnan(v))


def nanmean(v: np.ndarray) -> float:
    n = validate(v)
    if n <= 0:
        return np.nan
    return anys.nanmean(v)


def nanstd(v: np.ndarray) -> float:
    n = validate(v)
    if n <= 0:
        return np.nan
    return anys.nanstd(v, ddof=1)


def nanskew(v: np.ndarray) -> float:
    n = validate(v)
    if n <= 0:
        return np.nan
    if anys.allnan(v):
        return np.nan
    return skew(v, axis=None, bias=False, nan_policy="omit")


def nankurt(v: np.ndarray) -> float:
    n = validate(v)
    if n <= 0:
        return np.nan
    if anys.allnan(v):
        return np.nan
    return kurtosis(v, axis=None, fisher=True, bias=False, nan_policy="omit")


def nanpctl(v: np.ndarray, q: int) -> float:
    n = validate(v)
    if n <= 0:
        return np.nan
    if q <= 0:
        return anys.nanmin(v)
    if q >= 100:
        return anys.nanmax(v)
    if q == 50:
        return anys.nanmedian(v)
    if anys.allnan(v):
        return np.nan
    return np.nanpercentile(v, q)


def rolling_sum(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_sum(v, window)


def rolling_mean(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_mean(v, window)


def rolling_std(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_std(v, window, ddof=1)


def rolling_var(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_var(v, window, ddof=1)


def rolling_min(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_min(v, window)


def rolling_max(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_max(v, window)


def rolling_argmin(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_argmin(v, window)


def rolling_argmax(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_argmax(v, window)


def rolling_median(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_median(v, window)


def rolling_rank(v: np.ndarray, window: int) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    return anys.move_rank(v, window)


def rolling_apply(
    v: np.ndarray,
    window: int,
    func: Callable[[np.ndarray], float],
) -> np.ndarray:
    n = validate_rolling(v, window)
    if window == 0 or window > n:
        return nans(n)
    swv = sliding_window_view(v, window)
    ret = np.asarray([func(sw) for sw in swv], dtype=np.float64)
    assert ret.ndim == 1
    if window > 1:
        ret = np.concatenate((nans(window - 1), ret))
    return ret


###############################################################################
# price
###############################################################################


def price2relative(price: np.ndarray) -> np.ndarray:
    n = validate(price)
    if n <= 1:
        return nans(n)
    rel = price[1:] / price[:-1]
    return np.concatenate((nans(1), rel))


def price2sr(price: np.ndarray) -> np.ndarray:
    n = validate(price)
    if n <= 1:
        return nans(n)
    sr = price[1:] / price[:-1] - 1
    return np.concatenate((nans(1), sr))


def price2lr(price: np.ndarray) -> np.ndarray:
    n = validate(price)
    if n <= 1:
        return nans(n)
    lr = np.log(price[1:] / price[:-1])
    return np.concatenate((nans(1), lr))


def price_metrics(
    price: np.ndarray,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> np.ndarray:
    rel = price2relative(price)
    sr = rel - 1
    lr = np.log(rel)
    return lr_sr_metrics(lr, sr, ann_factor, sqrt_ann_factor, mode)


def price_terms_metrics(
    price: np.ndarray,
    terms: list[int],
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> np.ndarray:
    n = validate(price)
    rel = price2relative(price)
    sr = rel - 1
    lr = np.log(rel)
    if sqrt_ann_factor is None:
        sqrt_ann_factor = np.sqrt(ann_factor)
    nr = len(lr_sr_metrics_meta(mode))

    def metrics(term: int) -> np.ndarray:
        if term > n:
            return nans(nr)
        return lr_sr_metrics(
            lr[-term:], sr[-term:], ann_factor, sqrt_ann_factor, mode
        )

    return np.asarray([metrics(term) for term in terms], dtype=np.float64).T


###############################################################################
# sr
###############################################################################


def sr2lr(sr: np.ndarray) -> np.ndarray:
    n = validate(sr)
    if n <= 0:
        return nans(n)
    return anys.sr2lr(sr)


def sr_kelly_criterion(sr: np.ndarray, ann_factor: float) -> float:
    """
    Kelly Criterion with Empirical Distribution
    """
    n = validate(sr)
    if n <= 0:
        return np.nan

    min_sr = anys.nanmin(sr)
    max_sr = anys.nanmax(sr)
    if max_sr <= 0 or min_sr >= 0:
        return np.nan

    eps = 0.000001
    lb = -1 / max_sr
    ub = -1 / min_sr
    bounds = [(lb + eps, ub - eps)]
    x0 = zeros(1)
    result = minimize(
        lambda x: -anys.nanmean(np.log(sr * x[0] + 1)) * ann_factor,
        x0,
        method="SLSQP",
        bounds=bounds,
    )
    if result.success:
        return result.x[0]
    return np.nan


def sr_metrics(
    sr: np.ndarray,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> np.ndarray:
    return lr_sr_metrics(sr2lr(sr), sr, ann_factor, sqrt_ann_factor, mode)


###############################################################################
# lr
###############################################################################


def lr2sr(lr: np.ndarray) -> np.ndarray:
    n = validate(lr)
    if n <= 0:
        return nans(n)
    return anys.lr2sr(lr)


def lr2crdd(lr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = validate(lr)
    if n <= 0:
        return nans(n), nans(n)
    lr0_cr = np.nancumsum(lr)
    lr0_peak = np.maximum.accumulate(lr0_cr)
    lr0_dd = lr0_cr - lr0_peak
    return lr0_cr, lr0_dd


def lr_metrics(
    lr: np.ndarray,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> np.ndarray:
    return lr_sr_metrics(lr, lr2sr(lr), ann_factor, sqrt_ann_factor, mode)


###############################################################################
# lr & sr
###############################################################################


def lr_sr_metrics_meta(mode: int) -> dict[str, str]:
    if mode == 0:
        return {
            # Basic
            "SR_CR": "[SR] Cumulative Return = P(T) / P(0) - 1",
            "SR_AGR": "[SR] Annualized Growth Rate (aka. CAGR)",
            "SR_VOL": "[SR] Annualized Volatility",
            "SR_MDD": "[SR] Maximum Drawdown = min(SR_DD)",
            # Risk Adjusted Return
            "SR_SHARPE": "[SR] Sharpe Ratio = SR_AGR / SR_VOL",
            "SR_SORTINO": "[SR] Sortino Ratio = SR_AGR / SR_DVOL",
            "SR_CALMAR": "[SR] Calmar Ratio = SR_AGR / -SR_MDD",
        }
    if mode == 1:
        return {
            # Basic
            "LR_CR": "[LR] Cumulative Return = log(P(T) / P(0))",
            "LR_AGR": "[LR] Annualized Growth Rate",
            "LR_VOL": "[LR] Annualized Volatility",
            "LR_MDD": "[LR] Maximum Drawdown = min(LR_DD)",
            # Risk Adjusted Return
            "LR_SHARPE": "[LR] Sharpe Ratio = LR_AGR / LR_VOL",
            "LR_SORTINO": "[LR] Sortino Ratio = LR_AGR / LR_DVOL",
            "LR_CALMAR": "[LR] Calmar Ratio = LR_AGR / -LR_MDD",
        }
    return {
        # Basic
        "LR_CR": "[LR] Cumulative Return = log(P(T) / P(0))",
        "LR_AGR": "[LR] Annualized Growth Rate",
        "LR_VOL": "[LR] Annualized Volatility",
        "LR_MDD": "[LR] Maximum Drawdown = min(LR_DD)",
        # Risk Adjusted Return
        "LR_SHARPE": "[LR] Sharpe Ratio = LR_AGR / LR_VOL",
        "LR_SORTINO": "[LR] Sortino Ratio = LR_AGR / LR_DVOL",
        "LR_CALMAR": "[LR] Calmar Ratio = LR_AGR / -LR_MDD",
        "SR_KELLY": "[SR] Kelly Criterion",
        # Potential
        "LR_PAGR": "[LR] Potential Annualized Growth Rate",
        "LR_ARG/PAGR": "[LR] LR_ARG / LR_PAGR",
        # Ratio
        "LR_WINS/TOTALS": "[LR] Wins/Totals Ratio = LR_P_COUNT / LR_COUNT",
        "LR_LOSSES/WINS": "[LR] Losses/Wins Ratio = LR_L_COUNT / LR_P_COUNT",
        "LR_PROFIT/LOSS": "[LR] Profit/Loss Ratio = LR_P_MEAN / -LR_L_MEAN",
        "LR_PROFIT_FACTOR": "[LR] Profit Factor = LR_P_SUM / -LR_L_SUM",
        # Etc
        "LR_DVOL": "[LR] Annualized Downside Volatility",
        "LR_DD": "[LR] Drawdown = LR_CR - LR_PEAK",
        # Descriptive Statistics
        "LR_COUNT": "[LR] Count",
        "LR_MEAN": "[LR] Mean",
        "LR_STD": "[LR] Standard Deviation",
        "LR_SKEW": "[LR] Skewness",
        "LR_KURT": "[LR] Kurtosis",
        "LR_MIN": "[LR] Min",
        "LR_25%": "[LR] 25%",
        "LR_50%": "[LR] 50%",
        "LR_75%": "[LR] 75%",
        "LR_MAX": "[LR] Max",
    }


def lr_sr_metrics(
    lr: np.ndarray,
    sr: np.ndarray,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> np.ndarray:
    n_lr = validate(lr)
    n_sr = validate(sr)
    assert n_lr == n_sr
    if n_lr <= 0:
        return nans(len(lr_sr_metrics_meta(mode)))
    if sqrt_ann_factor is None:
        sqrt_ann_factor = np.sqrt(ann_factor)

    lr0_cr, lr0_dd = lr2crdd(lr)
    lr_cr = lr0_cr[-1]
    lr_mdd = anys.nanmin(lr0_dd)
    lr_mean = nanmean(lr)
    lr_agr = lr_mean * ann_factor
    if mode == 0:
        srl = sr[sr <= 0]
        sr_cr = anys.lr2sr(lr_cr)
        sr_agr = anys.lr2sr(lr_agr)
        sr_vol = nanstd(sr) * sqrt_ann_factor
        sr_dvol = nanstd(srl) * sqrt_ann_factor
        sr_mdd = anys.lr2sr(lr_mdd)
        sr_sharpe = scalar.div(sr_agr, sr_vol)
        sr_sortino = scalar.div(sr_agr, sr_dvol)
        sr_calmar = scalar.div(sr_agr, -sr_mdd)
        return np.asarray(
            [sr_cr, sr_agr, sr_vol, sr_mdd, sr_sharpe, sr_sortino, sr_calmar],
            dtype=np.float64,
        )

    lr_std = nanstd(lr)
    lr_vol = lr_std * sqrt_ann_factor
    lrl = lr[lr <= 0]
    lr_dvol = nanstd(lrl) * sqrt_ann_factor
    lr_sharpe = scalar.div(lr_agr, lr_vol)
    lr_sortino = scalar.div(lr_agr, lr_dvol)
    lr_calmar = scalar.div(lr_agr, -lr_mdd)
    if mode == 1:
        return np.asarray(
            [lr_cr, lr_agr, lr_vol, lr_mdd, lr_sharpe, lr_sortino, lr_calmar],
            dtype=np.float64,
        )

    lr_count = nancnt(lr)
    lrp = lr[lr > 0]
    lrp_count = nancnt(lrp)
    lrp_mean = nanmean(lrp)
    lrl_count = nancnt(lrl)
    lrl_mean = nanmean(lrl)
    lr_pagr = nanmean(np.abs(lr)) * ann_factor
    return np.asarray(
        [
            lr_cr,
            lr_agr,
            lr_vol,
            lr_mdd,
            lr_sharpe,
            lr_sortino,
            lr_calmar,
            sr_kelly_criterion(sr, ann_factor),
            lr_pagr,
            scalar.div(lr_agr, lr_pagr),
            scalar.div(lrp_count, lr_count),
            scalar.div(lrl_count, lrp_count),
            scalar.div(lrp_mean, -lrl_mean),
            scalar.div(lrp_mean * lrp_count, -lrl_mean * lrl_count),
            lr_dvol,
            lr0_dd[-1],
            lr_count,
            lr_mean,
            lr_std,
            nanskew(lr),
            nankurt(lr),
            nanpctl(lr, 0),
            nanpctl(lr, 25),
            nanpctl(lr, 50),
            nanpctl(lr, 75),
            nanpctl(lr, 100),
        ],
        dtype=np.float64,
    )
