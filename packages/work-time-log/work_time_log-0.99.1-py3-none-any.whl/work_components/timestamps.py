""" API wrapper and extension for datetime """

import datetime as dt


def date_equals(left: dt.date, right: dt.date):
    """Compare date equality of arbitrary date or datetime instances.
    Handles comparison of datetime to date."""
    if not isinstance(left, dt.date) or not isinstance(right, dt.date):
        raise TypeError("Expected instance of (subclass of) datetime.date.")
    return (left.year, left.month, left.day) == (right.year, right.month, right.day)
