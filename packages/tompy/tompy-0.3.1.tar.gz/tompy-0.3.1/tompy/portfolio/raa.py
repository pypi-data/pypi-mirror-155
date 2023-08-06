"""
Keller, Wouter J.,
Lazy Momentum with Growth-Trend timing:
Resilient Asset Allocation (RAA) (December 20, 2020).
Available at SSRN: https://ssrn.com/abstract=3752294 or http://dx.doi.org/10.2139/ssrn.3752294
"""

import numpy as np
import pandas as pd

from tompy import matrix
from tompy.portfolio.base import Base
from tompy.portfolio.vaa import vaa_momentum_13612w

UNRATE = "UNRATE"
CANARY = ["VWO", "BND"]
RISKY = ["QQQ", "GLD", "IEF", "TLT", "IWN"]
CASH = ["IEF", "TLT"]


def raa_momentum_ret(price: np.ndarray, month: int, window: int) -> np.ndarray:
    nr, nc = matrix.validate(price)
    w = 1 + month * window
    if w > nr:
        return matrix.nans(1, nc)
    p0 = price[-1, :]
    pw = price[-1 - month * window, :]
    return p0 / pw - 1


def _weight(
    in_p: np.ndarray,
    in_unrate: np.ndarray,
    in_canary: np.ndarray,
    out_risky: np.ndarray,
    out_cash: np.ndarray,
    w_risky: float,
    w_cash: float,
    n_tickers_out: int,
    month: int,
) -> np.ndarray:
    nr = in_p.shape[0]
    if 1 + month * 12 > nr:
        return np.full(n_tickers_out, np.nan)
    weight = np.zeros(n_tickers_out)
    unrate_ret12 = raa_momentum_ret(in_p[:, in_unrate], month, 12)
    if unrate_ret12[0] >= 0:
        canary_13612w = vaa_momentum_13612w(in_p[:, in_canary], month)
        if np.any(canary_13612w <= 0):
            weight[out_cash] = w_cash
            return weight
    weight[out_risky] = w_risky
    return weight


def _portfolio_weight(
    price: pd.DataFrame,
    unrate: str,
    canary: list[str],
    risky: list[str],
    cash: list[str],
    month: int,
) -> pd.DataFrame:
    canary = list(dict.fromkeys(canary))
    risk = list(dict.fromkeys(risky))
    cash = list(dict.fromkeys(cash))
    tickers_in = list(dict.fromkeys([unrate] + canary))
    tickers_out = list(dict.fromkeys(risk + cash))
    tickers_all = list(dict.fromkeys(tickers_in + tickers_out))
    price = price[tickers_all].dropna()
    n_tickers_in = len(tickers_in)
    n_tickers_out = len(tickers_out)
    in_idx = np.asarray(range(n_tickers_in), dtype=int)
    out_idx = np.asarray(range(n_tickers_out), dtype=int)
    in_unrate = in_idx[[i in [unrate] for i in tickers_in]]
    in_canary = in_idx[[i in canary for i in tickers_in]]
    out_risky = out_idx[[i in risky for i in tickers_out]]
    out_cash = out_idx[[i in cash for i in tickers_out]]
    w_risky = 1 / len(risky)
    w_cash = 1 / len(cash)

    def __weight(in_p: np.ndarray) -> np.ndarray:
        return _weight(
            in_p,
            in_unrate,
            in_canary,
            out_risky,
            out_cash,
            w_risky,
            w_cash,
            n_tickers_out,
            month,
        )

    m = matrix.rolling_apply(
        price[tickers_in].values,
        1 + month * 12,
        __weight,
        n_tickers_out,
    )
    return pd.DataFrame(data=m, index=price.index, columns=tickers_out)


class RAA(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        ann_factor: float,
        unrate: str,
        canary: list[str],
        risky: list[str],
        cash: list[str],
    ):
        super().__init__(price, ann_factor)
        self.unrate = unrate
        self.canary = list(dict.fromkeys(canary))
        self.risky = list(dict.fromkeys(risky))
        self.cash = list(dict.fromkeys(cash))

    def portfolio_weight(self) -> pd.DataFrame:
        return _portfolio_weight(
            self.price,
            self.unrate,
            self.canary,
            self.risky,
            self.cash,
            int(self.ann_factor / 12),
        )
