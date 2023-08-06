"""
Keller, Wouter J. and Keuning, Jan Willem,
Protective Asset Allocation (PAA):
A Simple Momentum-Based Alternative for Term Deposits (April 5, 2016).
Available at SSRN: https://ssrn.com/abstract=2759734 or http://dx.doi.org/10.2139/ssrn.2759734
"""

import numpy as np
import pandas as pd

from tompy import anys, matrix, scalar
from tompy.portfolio.base import Base

C1 = ["IEF"]
G12 = [
    "SPY",
    "QQQ",
    "IWM",
    "VGK",
    "EWJ",
    "EEM",
    "IYR",
    "GSG",
    "GLD",
    "HYG",
    "LQD",
    "TLT",
]
G12_T = 6
A0 = 0
A1 = 1
A2 = 2


def paa_momentum_sma(price: np.ndarray, month: int, window: int) -> np.ndarray:
    nr, nc = matrix.validate_rolling(price, window)
    w = 1 + month * (window - 1)
    if w > nr:
        return matrix.nans(1, nc)
    p0 = price[-1, :]
    psma = matrix.nanmean(price[[-1 - month * i for i in range(window)], :])
    return p0 / psma - 1


def paa_bond_fraction(N: int, n: int, a: int) -> float:
    n1 = a * N / 4
    if n <= n1:
        return 1
    return scalar.div(N - n, N - n1)


def _weight(
    in_p: np.ndarray,
    io_risky: np.ndarray,
    io_cash: np.ndarray,
    n_tickers_out: int,
    month: int,
    T: int,
    N: int,
    A: int,
) -> np.ndarray:
    nr = in_p.shape[0]
    if 1 + month * 12 > nr:
        return np.full(n_tickers_out, np.nan)
    weight = np.zeros(n_tickers_out)

    risky_sma13 = paa_momentum_sma(in_p[:, io_risky], month, 13)
    n = anys.nansum(risky_sma13 > 0)
    bf = paa_bond_fraction(N, n, A)
    riskf = 1 - bf

    t = min(T, n)
    if t > 0:
        w_risky = riskf / t
        risky_sort = np.argsort(risky_sma13)
        for i in range(t):
            weight[io_risky[risky_sort[-1 - i]]] = w_risky

    if bf > 0:
        cash_sma13 = paa_momentum_sma(in_p[:, io_cash], month, 13)
        cash_sort = np.argsort(cash_sma13)
        weight[io_cash[cash_sort[-1]]] = bf
    return weight


def _portfolio_weight(
    price: pd.DataFrame,
    risky: list[str],
    cash: list[str],
    month: int,
    T: int,
    A: int,
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
    N = len(risky)

    def __weight(in_p: np.ndarray) -> np.ndarray:
        return _weight(
            in_p,
            io_risky,
            io_cash,
            n_tickers_out,
            month,
            T,
            N,
            A,
        )

    m = matrix.rolling_apply(
        price[tickers_in].values,
        1 + month * 12,
        __weight,
        n_tickers_out,
    )
    return pd.DataFrame(data=m, index=price.index, columns=tickers_out)


class PAA(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        ann_factor: float,
        risky: list[str],
        cash: list[str],
        T: int,
        A: int,
    ):
        super().__init__(price, ann_factor)
        self.risky = list(dict.fromkeys(risky))
        self.cash = list(dict.fromkeys(cash))
        self.T = T
        self.A = A

    def portfolio_weight(self) -> pd.DataFrame:
        return _portfolio_weight(
            self.price,
            self.risky,
            self.cash,
            int(self.ann_factor / 12),
            self.T,
            self.A,
        )
