from typing import Any, Optional

import bottleneck as bn
import numpy as np


def nansum(a: Any, axis: Optional[int] = None) -> Any:
    return bn.nansum(a, axis=axis)


def nanmean(a: Any, axis: Optional[int] = None) -> Any:
    return bn.nanmean(a, axis=axis)


def nanstd(a: Any, axis: Optional[int] = None, ddof: int = 1) -> Any:
    return bn.nanstd(a, axis=axis, ddof=ddof)


def nanvar(a: Any, axis: Optional[int] = None, ddof: int = 1) -> Any:
    return bn.nanvar(a, axis=axis, ddof=ddof)


def nanmin(a: Any, axis: Optional[int] = None) -> Any:
    return bn.nanmin(a, axis=axis)


def nanmax(a: Any, axis: Optional[int] = None) -> Any:
    return bn.nanmax(a, axis=axis)


def nanmedian(a: Any, axis: Optional[int] = None) -> Any:
    return bn.nanmedian(a, axis=axis)


def nanargmin(a: Any, axis: Optional[int] = None) -> Any:
    return bn.nanargmin(a, axis=axis)


def nanargmax(a: Any, axis: Optional[int] = None) -> Any:
    return bn.nanargmax(a, axis=axis)


def anynan(a: Any, axis: Optional[int] = None) -> Any:
    return bn.anynan(a, axis=axis)


def allnan(a: Any, axis: Optional[int] = None) -> Any:
    return bn.allnan(a, axis=axis)


def move_sum(
    a: Any, window: int, min_count: Optional[int] = None, axis: int = -1
) -> Any:
    return bn.move_sum(a, window, min_count=min_count, axis=axis)


def move_mean(
    a: Any, window: int, min_count: Optional[int] = None, axis: int = -1
) -> Any:
    return bn.move_mean(a, window, min_count=min_count, axis=axis)


def move_std(
    a: Any,
    window: int,
    min_count: Optional[int] = None,
    axis: int = -1,
    ddof: int = 1,
) -> Any:
    return bn.move_std(a, window, min_count=min_count, axis=axis, ddof=ddof)


def move_var(
    a: Any,
    window: int,
    min_count: Optional[int] = None,
    axis: int = -1,
    ddof: int = 1,
) -> Any:
    return bn.move_var(a, window, min_count=min_count, axis=axis, ddof=ddof)


def move_min(
    a: Any, window: int, min_count: Optional[int] = None, axis: int = -1
) -> Any:
    return bn.move_min(a, window, min_count=min_count, axis=axis)


def move_max(
    a: Any, window: int, min_count: Optional[int] = None, axis: int = -1
) -> Any:
    return bn.move_max(a, window, min_count=min_count, axis=axis)


def move_argmin(
    a: Any, window: int, min_count: Optional[int] = None, axis: int = -1
) -> Any:
    return bn.move_argmin(a, window, min_count=min_count, axis=axis)


def move_argmax(
    a: Any, window: int, min_count: Optional[int] = None, axis: int = -1
) -> Any:
    return bn.move_argmax(a, window, min_count=min_count, axis=axis)


def move_median(
    a: Any, window: int, min_count: Optional[int] = None, axis: int = -1
) -> Any:
    return bn.move_median(a, window, min_count=min_count, axis=axis)


def move_rank(
    a: Any, window: int, min_count: Optional[int] = None, axis: int = -1
) -> Any:
    return bn.move_rank(a, window, min_count=min_count, axis=axis)


def sr2lr(sr: Any) -> Any:
    return np.log(sr + 1)


def lr2sr(lr: Any) -> Any:
    return np.exp(lr) - 1
