from typing import Optional

import numpy as np
import pandas as pd

from tompy import dataframe


def rebalancing_weight(
    weights: pd.DataFrame,
    rebalancing: str,
    lag: int,
) -> pd.DataFrame:
    if rebalancing == "W":
        idx = pd.DataFrame(index=weights.index)
        idx["W"] = idx.index.dayofweek
        idx["NA"] = idx["W"].diff(-1).fillna(0) <= 0
        weights = weights.copy()
        weights.loc[idx["NA"]] = np.nan
    elif rebalancing == "M":
        idx = pd.DataFrame(index=weights.index)
        idx["M"] = idx.index.month
        idx["NA"] = idx["M"].diff(-1).fillna(0) == 0
        weights = weights.copy()
        weights.loc[idx["NA"]] = np.nan
    return dataframe.shift(weights, lag)


class Base:
    def __init__(
        self,
        price: pd.DataFrame,
        ann_factor: float,
    ) -> None:
        self.price = price
        self.ann_factor = ann_factor

    def portfolio_weight(self) -> pd.DataFrame:
        assert False
        return pd.DataFrame(index=self.price.index)

    def rebalancing_weight(
        self,
        weights: Optional[pd.DataFrame] = None,
        rebalancing: str = "D",
        lag: int = 1,
    ) -> pd.DataFrame:
        if weights is None:
            weights = self.portfolio_weight()
        return rebalancing_weight(weights, rebalancing, lag)

    def portfolio_price(
        self,
        weights: pd.DataFrame,
        fee_rate: float,
    ) -> pd.Series:
        return dataframe.portfolio_price(self.price, weights, fee_rate)
