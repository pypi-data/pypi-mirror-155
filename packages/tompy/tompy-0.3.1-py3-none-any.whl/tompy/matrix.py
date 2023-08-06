from typing import Callable, Optional

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.stats import kurtosis, skew

from tompy import anys, vector

###############################################################################
# matrix
###############################################################################


def validate(m: np.ndarray) -> tuple[int, int]:
    assert m.ndim == 2
    return m.shape


def validate_rolling(m: np.ndarray, window: int) -> tuple[int, int]:
    assert window >= 0
    return validate(m)


def zeros(nr: int, nc: int) -> np.ndarray:
    return np.zeros((nr, nc), dtype=np.float64)


def nans(nr: int, nc: int) -> np.ndarray:
    return np.full((nr, nc), np.nan, dtype=np.float64)


def describe_meta() -> dict[str, str]:
    return vector.describe_meta()


def describe(m: np.ndarray) -> np.ndarray:
    nr, nc = validate(m)
    if nr <= 0:
        return nans(len(describe_meta()), nc)
    return np.asarray(
        [
            nancnt(m),
            nanmean(m),
            nanstd(m),
            nanskew(m),
            nankurt(m),
            nanpctl(m, 0),
            nanpctl(m, 25),
            nanpctl(m, 50),
            nanpctl(m, 75),
            nanpctl(m, 100),
        ],
        dtype=np.float64,
    )


def shift(m: np.ndarray, lag: int) -> np.ndarray:
    nr, nc = validate(m)
    if nr <= 0 or lag == 0:
        return m
    if lag > 0:
        if lag >= nr:
            return nans(nr, nc)
        return np.concatenate((nans(lag, nc), m[:-lag, :]))
    lag = -lag
    if lag >= nr:
        return nans(nr, nc)
    return np.concatenate((m[lag:, :], nans(lag, nc)))


def nancnt(m: np.ndarray) -> np.ndarray:
    nr, nc = validate(m)
    if nr <= 0:
        return nans(0, nc)
    return nr - anys.nansum(np.isnan(m), axis=0)


def nanmean(m: np.ndarray) -> np.ndarray:
    nr, nc = validate(m)
    if nr <= 0:
        return nans(0, nc)
    return anys.nanmean(m, axis=0)


def nanstd(m: np.ndarray) -> np.ndarray:
    nr, nc = validate(m)
    if nr <= 0:
        return nans(0, nc)
    return anys.nanstd(m, axis=0, ddof=1)


def nanskew(m: np.ndarray) -> np.ndarray:
    nr, nc = validate(m)
    if nr <= 0:
        return nans(0, nc)
    if anys.allnan(m):
        return nans(1, nc)
    return skew(m, axis=0, bias=False, nan_policy="omit")


def nankurt(m: np.ndarray) -> np.ndarray:
    nr, nc = validate(m)
    if nr <= 0:
        return nans(0, nc)
    if anys.allnan(m):
        return nans(1, nc)
    return kurtosis(m, axis=0, fisher=True, bias=False, nan_policy="omit")


def nanpctl(m: np.ndarray, q: int) -> float:
    nr, nc = validate(m)
    if nr <= 0:
        return nans(0, nc)
    if q <= 0:
        return anys.nanmin(m, axis=0)
    if q >= 100:
        return anys.nanmax(m, axis=0)
    if q == 50:
        return anys.nanmedian(m, axis=0)
    if anys.allnan(m):
        return nans(1, nc)
    return np.nanpercentile(m, q, axis=0)


def rolling_sum(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_sum(m, window, axis=0)


def rolling_mean(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_mean(m, window, axis=0)


def rolling_std(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_std(m, window, axis=0, ddof=1)


def rolling_var(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_var(m, window, axis=0, ddof=1)


def rolling_min(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_min(m, window, axis=0)


def rolling_max(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_max(m, window, axis=0)


def rolling_argmin(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_argmin(m, window, axis=0)


def rolling_argmax(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_argmax(m, window, axis=0)


def rolling_median(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_median(m, window, axis=0)


def rolling_rank(m: np.ndarray, window: int) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nc)
    return anys.move_rank(m, window, axis=0)


def rolling_apply(
    m: np.ndarray,
    window: int,
    func: Callable[[np.ndarray], np.ndarray],
    nfout: int,
) -> np.ndarray:
    nr, nc = validate_rolling(m, window)
    if window == 0 or window > nr:
        return nans(nr, nfout)
    swv = sliding_window_view(m, (window, nc)).reshape((-1, window, nc))
    ret = np.asarray([func(sw) for sw in swv], dtype=np.float64)
    assert ret.ndim == 2 and ret.shape[1] == nfout
    if window > 1:
        ret = np.concatenate((nans(window - 1, nfout), ret))
    return ret


###############################################################################
# price
###############################################################################


def price2relative(price: np.ndarray) -> np.ndarray:
    nr, nc = validate(price)
    if nr <= 1 or nc <= 0:
        return nans(nr, nc)
    rel = price[1:, :] / price[:-1, :]
    return np.concatenate((nans(1, nc), rel))


def price2sr(price: np.ndarray) -> np.ndarray:
    nr, nc = validate(price)
    if nr <= 1 or nc <= 0:
        return nans(nr, nc)
    sr = price[1:, :] / price[:-1, :] - 1
    return np.concatenate((nans(1, nc), sr))


def price2lr(price: np.ndarray) -> np.ndarray:
    nr, nc = validate(price)
    if nr <= 1 or nc <= 0:
        return nans(nr, nc)
    lr = np.log(price[1:, :] / price[:-1, :])
    return np.concatenate((nans(1, nc), lr))


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


###############################################################################
# sr
###############################################################################


def sr2lr(sr: np.ndarray) -> np.ndarray:
    nr, nc = validate(sr)
    if nr <= 0:
        return nans(nr, nc)
    return anys.sr2lr(sr)


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
    nr, nc = validate(lr)
    if nr <= 0:
        return nans(nr, nc)
    return anys.lr2sr(lr)


def lr2crdd(lr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    nr, nc = validate(lr)
    if nr <= 0:
        return nans(nr, nc), nans(nr, nc)
    lr0_cr = np.nancumsum(lr, axis=0)
    lr0_peak = np.maximum.accumulate(lr0_cr, axis=0)
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
    return vector.lr_sr_metrics_meta(mode)


def lr_sr_metrics(
    lr: np.ndarray,
    sr: np.ndarray,
    ann_factor: float,
    sqrt_ann_factor: Optional[float] = None,
    mode: int = 0,
) -> np.ndarray:
    nr_lr, nc_lr = validate(lr)
    nr_sr, nc_sr = validate(sr)
    assert nr_lr == nr_sr and nc_lr == nc_sr
    if nr_lr <= 0:
        return nans(len(lr_sr_metrics_meta(mode)), nc_lr)
    if sqrt_ann_factor is None:
        sqrt_ann_factor = np.sqrt(ann_factor)
    return np.asarray(
        [
            vector.lr_sr_metrics(
                lr[:, i], sr[:, i], ann_factor, sqrt_ann_factor, mode
            )
            for i in range(nc_lr)
        ],
        dtype=np.float64,
    ).T


###############################################################################
# portfolio
###############################################################################


def portfolio_price(
    price: np.ndarray, weight: np.ndarray, fee_rate: float
) -> np.ndarray:
    price_shape = validate(price)
    weight_shape = validate(weight)
    assert price_shape == weight_shape
    nr, nc = weight_shape
    nav = 1
    position_quantity = vector.zeros(nc)
    cash = 1
    navs = vector.zeros(nr)
    for i in range(nr):
        pi = price[i]
        wi = weight[i]
        nav = cash + anys.nansum(position_quantity * pi)
        if not anys.allnan(wi):
            target_position_dollar = nav * wi
            target_position_quantity = target_position_dollar / pi
            trading_position_quantity = (
                target_position_quantity - position_quantity
            )
            trading_position_dollar = trading_position_quantity * pi
            trading_fee = (
                anys.nansum(np.abs(trading_position_dollar)) * fee_rate
            )
            nav = (
                cash
                - anys.nansum(trading_position_dollar)
                + anys.nansum(target_position_dollar)
                - trading_fee
            )
            position_dollar = nav * wi
            position_quantity = position_dollar / pi
            cash = nav - anys.nansum(position_dollar)
        navs[i] = nav
    return navs
