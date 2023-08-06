import numpy as np


def div(dividend: float, divisor: float) -> float:
    if divisor == 0:
        return np.nan
    return dividend / divisor


def kelly_criterion(p: float, a: float, b: float) -> float:
    """
    Kelly Criterion with Bernoulli Distribution
    p is the probability that the investment increases in value.
    a is the fraction that is lost in a negative outcome.
    b is the fraction that is gained in a positive outcome.
    """
    if a == 0 or b == 0:
        return np.nan
    q = 1 - p
    f = p / a - q / b
    return f
