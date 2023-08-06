import numpy as np
import pandas as pd

from tompy.portfolio.base import Base


def crp_ew(price: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    price = price[tickers].dropna()
    nr = price.shape[0]
    nc = len(tickers)
    ew = 1.0 / nc
    m = np.full((nr, nc), ew)
    return pd.DataFrame(data=m, index=price.index, columns=tickers)


def crp(price: pd.DataFrame, ticker_weights: dict[str, float]) -> pd.DataFrame:
    tickers = list(ticker_weights.keys())
    weights = list(ticker_weights.values())
    price = price[tickers].dropna()
    nr = price.shape[0]
    m = np.tile(weights, (nr, 1))
    return pd.DataFrame(data=m, index=price.index, columns=tickers)


class CRP_EW(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        ann_factor: float,
        tickers: list[str],
    ) -> None:
        super().__init__(price, ann_factor)
        self.tickers = list(dict.fromkeys(tickers))

    def portfolio_weight(self) -> pd.DataFrame:
        return crp_ew(self.price, self.tickers)


class CRP(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        ann_factor: float,
        ticker_weights: dict[str, float],
    ) -> None:
        super().__init__(price, ann_factor)
        self.ticker_weights = ticker_weights

    def portfolio_weight(self) -> pd.DataFrame:
        return crp(self.price, self.ticker_weights)
