"""
Date helpers.
"""
from datetime import date


def is_weekend(day: date):
    """
    Say if this day is a weekend or not.

    Parameters
    ----------
        day: date
            Day.

    Returns
    -------
        bool
            True if is weekend.
    """
    return day.weekday() in [5, 6]
