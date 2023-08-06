"""
Keller, Wouter J. and Keuning, Jan Willem,
Breadth Momentum and the Canary Universe:
Defensive Asset Allocation (DAA) (July 12, 2018).
Available at SSRN: https://ssrn.com/abstract=3212862 or http://dx.doi.org/10.2139/ssrn.3212862
"""

import numpy as np
import pandas as pd

from tompy import anys, matrix
from tompy.portfolio.base import Base
from tompy.portfolio.vaa import vaa_cash_fraction, vaa_momentum_13612w

P2 = ["VWO", "BND"]
C3 = ["SHY", "IEF", "LQD"]
G12 = [
    "SPY",
    "IWM",
    "QQQ",
    "VGK",
    "EWJ",
    "VWO",
    "VNQ",
    "GSG",
    "GLD",
    "TLT",
    "HYG",
    "LQD",
]
G12_T = 6
G12_B = 2
G4 = ["SPY", "VEA", "VWO", "BND"]
G4_T = 4
G4_B = 2


def _weight(
    in_p: np.ndarray,
    in_canary: np.ndarray,
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

    canary_13612w = vaa_momentum_13612w(in_p[:, in_canary], month)
    b = anys.nansum(canary_13612w <= 0)
    cf = vaa_cash_fraction(B, b)
    riskf = 1 - cf

    risky_13612w = vaa_momentum_13612w(in_p[:, io_risky], month)
    t = min(int(T * riskf), anys.nansum(risky_13612w > 0))
    if t > 0:
        w_risky = riskf / t
        risky_sort = np.argsort(risky_13612w)
        for i in range(t):
            weight[io_risky[risky_sort[-1 - i]]] = w_risky
    else:
        cf = 1

    if cf > 0:
        cash_13612w = vaa_momentum_13612w(in_p[:, io_cash], month)
        cash_sort = np.argsort(cash_13612w)
        weight[io_cash[cash_sort[-1]]] = cf
    return weight


def _portfolio_weight(
    price: pd.DataFrame,
    canary: list[str],
    risky: list[str],
    cash: list[str],
    month: int,
    T: int,
    B: int,
) -> pd.DataFrame:
    canary = list(dict.fromkeys(canary))
    risky = list(dict.fromkeys(risky))
    cash = list(dict.fromkeys(cash))
    tickers_out = list(dict.fromkeys(risky + cash))
    tickers_in = list(dict.fromkeys(tickers_out + canary))
    tickers_all = list(dict.fromkeys(tickers_in + tickers_out))
    price = price[tickers_all].dropna()
    n_tickers_in = len(tickers_in)
    n_tickers_out = len(tickers_out)
    in_idx = np.asarray(range(n_tickers_in), dtype=int)
    out_idx = np.asarray(range(n_tickers_out), dtype=int)
    in_canary = in_idx[[i in canary for i in tickers_in]]
    io_risky = out_idx[[i in risky for i in tickers_out]]
    io_cash = out_idx[[i in cash for i in tickers_out]]

    def __weight(in_p: np.ndarray) -> np.ndarray:
        return _weight(
            in_p,
            in_canary,
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


class DAA(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        ann_factor: float,
        canary: list[str],
        risky: list[str],
        cash: list[str],
        T: int,
        B: int,
    ):
        super().__init__(price, ann_factor)
        self.canary = list(dict.fromkeys(canary))
        self.risky = list(dict.fromkeys(risky))
        self.cash = list(dict.fromkeys(cash))
        self.T = T
        self.B = B

    def portfolio_weight(self) -> pd.DataFrame:
        return _portfolio_weight(
            self.price,
            self.canary,
            self.risky,
            self.cash,
            int(self.ann_factor / 12),
            self.T,
            self.B,
        )
