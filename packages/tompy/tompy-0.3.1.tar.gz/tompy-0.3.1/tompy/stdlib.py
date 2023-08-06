import asyncio
import datetime
from functools import wraps
from typing import Any, Awaitable, Callable, Optional

import pytz

###############################################################################
# datetime
###############################################################################


def datetime_now(tz: Optional[pytz.BaseTzInfo] = None) -> datetime.datetime:
    """
    Return the current timezone datetime.
    """
    utcnow = pytz.utc.localize(datetime.datetime.utcnow())
    if tz is not None:
        return utcnow.astimezone(tz)
    return utcnow


###############################################################################
# date
###############################################################################


def date(year: int, month: int, day: int) -> datetime.date:
    return datetime.date(year, month, day)


def date_today(tz: Optional[pytz.BaseTzInfo] = None) -> datetime.date:
    """
    Return the current timezone date.
    """
    return datetime_now(tz=tz).date()


def date_add(d: datetime.date, days: int) -> datetime.date:
    """
    days range: -999999999 <= days <= 999999999
    """
    return d + datetime.timedelta(days=days)


def date_weekday(d: datetime.date) -> int:
    """
    Return the day of the week as an integer, Monday is 0 and Sunday is 6.
    """
    return d.weekday()


def date_is_weekend(d: datetime.date) -> bool:
    return date_weekday(d) > 4


def date_str(d: datetime.date) -> str:
    """
    Return a string representing the date in ISO 8601 format, YYYY-MM-DD.
    """
    return d.isoformat()


def date_from_str(datestr: str, fmt: str = "%Y-%m-%d") -> datetime.date:
    return datetime.datetime.strptime(datestr, fmt).date()


###############################################################################
# Decorator
###############################################################################


def sync(async_func: Callable[..., Awaitable[Any]]) -> Callable[..., Any]:
    """
    Decorator Sync
    """

    @wraps(async_func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(async_func(*args, **kwargs))

    return wrapper
