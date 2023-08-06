"""
Keller, Wouter J.,
Growth-Trend Timing and 60-40 Variations:
Lethargic Asset Allocation (LAA) (December 4, 2019).
Available at SSRN: https://ssrn.com/abstract=3498092 or http://dx.doi.org/10.2139/ssrn.3498092
"""

import numpy as np
import pandas as pd

from tompy import matrix
from tompy.portfolio.base import Base
from tompy.portfolio.paa import paa_momentum_sma

UNRATE = "UNRATE"
SPY = "SPY"
RISKY = ["QQQ", "IWD", "GLD", "IEF"]
CASH = ["SHY", "IWD", "GLD", "IEF"]


def _weight(
    in_p: np.ndarray,
    in_unrate: np.ndarray,
    in_spy: np.ndarray,
    out_risky: np.ndarray,
    out_cash: np.ndarray,
    w_risky: float,
    w_cash: float,
    n_tickers_out: int,
    month: int,
) -> np.ndarray:
    nr = in_p.shape[0]
    if 1 + month * (12 - 1) > nr:
        return np.full(n_tickers_out, np.nan)
    weight = np.zeros(n_tickers_out)
    unrate_sma12 = paa_momentum_sma(in_p[:, in_unrate], month, 12)
    if unrate_sma12[0] >= 0:
        spy_sma10 = paa_momentum_sma(in_p[:, in_spy], month, 10)
        if spy_sma10[0] <= 0:
            weight[out_cash] = w_cash
            return weight
    weight[out_risky] = w_risky
    return weight


def _portfolio_weight(
    price: pd.DataFrame,
    unrate: str,
    spy: str,
    risky: list[str],
    cash: list[str],
    month: int,
) -> pd.DataFrame:
    risky = list(dict.fromkeys(risky))
    cash = list(dict.fromkeys(cash))
    tickers_in = list(dict.fromkeys([unrate, spy]))
    tickers_out = list(dict.fromkeys(risky + cash))
    tickers_all = list(dict.fromkeys(tickers_in + tickers_out))
    price = price[tickers_all].dropna()
    n_tickers_in = len(tickers_in)
    n_tickers_out = len(tickers_out)
    in_idx = np.asarray(range(n_tickers_in), dtype=int)
    out_idx = np.asarray(range(n_tickers_out), dtype=int)
    in_unrate = in_idx[[i in [unrate] for i in tickers_in]]
    in_spy = in_idx[[i in [spy] for i in tickers_in]]
    out_risky = out_idx[[i in risky for i in tickers_out]]
    out_cash = out_idx[[i in cash for i in tickers_out]]
    w_risky = 1 / len(risky)
    w_cash = 1 / len(cash)

    def __weight(in_p: np.ndarray) -> np.ndarray:
        return _weight(
            in_p,
            in_unrate,
            in_spy,
            out_risky,
            out_cash,
            w_risky,
            w_cash,
            n_tickers_out,
            month,
        )

    m = matrix.rolling_apply(
        price[tickers_in].values,
        1 + month * (12 - 1),
        __weight,
        n_tickers_out,
    )
    return pd.DataFrame(data=m, index=price.index, columns=tickers_out)


class LAA(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        ann_factor: float,
        unrate: str,
        spy: str,
        risky: list[str],
        cash: list[str],
    ):
        super().__init__(price, ann_factor)
        self.unrate = unrate
        self.spy = spy
        self.risky = list(dict.fromkeys(risky))
        self.cash = list(dict.fromkeys(cash))

    def portfolio_weight(self) -> pd.DataFrame:
        return _portfolio_weight(
            self.price,
            self.unrate,
            self.spy,
            self.risky,
            self.cash,
            int(self.ann_factor / 12),
        )
