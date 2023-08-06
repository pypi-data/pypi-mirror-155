"""
Keller, Wouter J. and Keuning, Jan Willem,
Breadth Momentum and Vigilant Asset Allocation (VAA):
Winning More by Losing Less (July 14, 2017).
Available at SSRN: https://ssrn.com/abstract=3002624 or http://dx.doi.org/10.2139/ssrn.3002624
"""

import numpy as np
import pandas as pd

from tompy import anys, matrix, scalar
from tompy.portfolio.base import Base

C3 = ["SHY", "IEF", "LQD"]
G12 = [
    "SPY",
    "IWM",
    "QQQ",
    "VGK",
    "EWJ",
    "EEM",
    "IYR",
    "GSG",
    "GLD",
    "TLT",
    "LQD",
    "HYG",
]
G12_T = 2
G12_B = 4
G4 = ["SPY", "EFA", "EEM", "AGG"]
G4_T = 1
G4_B = 1


def vaa_momentum_13612w(price: np.ndarray, month: int) -> np.ndarray:
    nr, nc = matrix.validate(price)
    w = 1 + month * 12
    if w > nr:
        return matrix.nans(1, nc)
    p0 = price[-1, :]
    p1 = price[-1 - month, :]
    p3 = price[-1 - month * 3, :]
    p6 = price[-1 - month * 6, :]
    p12 = price[-1 - month * 12, :]
    return 12 * p0 / p1 + 4 * p0 / p3 + 2 * p0 / p6 + p0 / p12 - 19


def vaa_cash_fraction(B: int, b: int) -> float:
    if b >= B:
        return 1
    return scalar.div(b, B)


def _weight(
    in_p: np.ndarray,
    io_risky: np.ndarray,
    io_cash: np.ndarray,
    n_tickers_out: int,
    month: int,
    T: int,
    B: int,
) -> np.ndarray:
    nr = in_p.shape[0]
    if 1 + month * 12 > nr:
        return np.full(n_tickers_out, np.nan)
    weight = np.zeros(n_tickers_out)

    risky_13612w = vaa_momentum_13612w(in_p[:, io_risky], month)
    b = anys.nansum(risky_13612w <= 0)
    cf = vaa_cash_fraction(B, b)
    riskf = 1 - cf

    t = min(T, anys.nansum(risky_13612w > 0))
    if t > 0:
        w_risky = riskf / t
        risky_sort = np.argsort(risky_13612w)
        for i in range(t):
            weight[io_risky[risky_sort[-1 - i]]] = w_risky

    if cf > 0:
        cash_13612w = vaa_momentum_13612w(in_p[:, io_cash], month)
        cash_sort = np.argsort(cash_13612w)
        weight[io_cash[cash_sort[-1]]] = cf
    return weight


def _portfolio_weight(
    price: pd.DataFrame,
    risky: list[str],
    cash: list[str],
    month: int,
    T: int,
    B: int,
) -> pd.DataFrame:
    risky = list(dict.fromkeys(risky))
    cash = list(dict.fromkeys(cash))
    tickers_out = list(dict.fromkeys(risky + cash))
    tickers_in = tickers_out
    tickers_all = tickers_out
    price = price[tickers_all].dropna()
    n_tickers_out = len(tickers_out)
    out_idx = np.asarray(range(n_tickers_out), dtype=int)
    io_risky = out_idx[[i in risky for i in tickers_out]]
    io_cash = out_idx[[i in cash for i in tickers_out]]

    def __weight(in_p: np.ndarray) -> np.ndarray:
        return _weight(
            in_p,
            io_risky,
            io_cash,
            n_tickers_out,
            month,
            T,
            B,
        )

    m = matrix.rolling_apply(
        price[tickers_in].values,
        1 + month * 12,
        __weight,
        n_tickers_out,
    )
    return pd.DataFrame(data=m, index=price.index, columns=tickers_out)


class VAA(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        ann_factor: float,
        risky: list[str],
        cash: list[str],
        T: int,
        B: int,
    ):
        super().__init__(price, ann_factor)
        self.risky = list(dict.fromkeys(risky))
        self.cash = list(dict.fromkeys(cash))
        self.T = T
        self.B = B

    def portfolio_weight(self) -> pd.DataFrame:
        return _portfolio_weight(
            self.price,
            self.risky,
            self.cash,
            int(self.ann_factor / 12),
            self.T,
            self.B,
        )
