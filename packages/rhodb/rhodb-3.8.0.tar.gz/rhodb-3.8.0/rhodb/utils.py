import datetime


def stringify_dates(x):
    """ Method that returns a string representation of a date.
        Useful for JSON serialization.
    """

    if isinstance(x, (datetime.datetime, datetime.date, datetime.time)):
        return x.isoformat()
    elif isinstance(x, datetime.timedelta):
        return x.total_seconds()
    return x
