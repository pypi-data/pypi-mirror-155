import datetime
from dateutil.relativedelta import relativedelta


def get_date_now():
    return datetime.date.today()


def get_datetime_now():
    return datetime.datetime.now()


def format_datetime(dt, include_time: bool = True, include_ms: bool = False) -> str:
    output = str(dt.isoformat())

    # Outputter
    if not include_time:
        return output.split("T")[0]
    elif not include_ms:
        return output.split(".")[0]
    return output


def parse_past_date_text(past_date_text: str, include_time: bool = True, include_ms: bool = False) -> str:
    """
    Input: 3 months ago
    Output: 2022-06-12T16:33:23.881970
    @see: https://stackoverflow.com/a/43139770
    """
    dateTextParts = past_date_text.split()
    partsLength = len(dateTextParts)

    if partsLength < 2:
        raise Exception(f"Invalid date text pattern: {past_date_text}")

    # Special amount indicators
    if dateTextParts[0] in ["last", "prev", "previous"]:
        dateTextParts[0] = 1

    if partsLength == 1 and dateTextParts[0].lower() == "today":
        return format_datetime(datetime.datetime.now(), include_time=include_time, include_ms=include_ms)
    elif partsLength == 1 and dateTextParts[0].lower() == "yesterday":
        date = datetime.datetime.now() - relativedelta(days=1)
        return format_datetime(date, include_time=include_time, include_ms=include_ms)
    elif dateTextParts[1].lower() in ["sec", "secs", "second", "seconds", "s"]:
        date = datetime.datetime.now() - relativedelta(hours=int(dateTextParts[0]))
        return format_datetime(date, include_time=include_time, include_ms=include_ms)
    elif dateTextParts[1].lower() in ["hour", "hours", "hr", "hrs", "h"]:
        date = datetime.datetime.now() - relativedelta(hours=int(dateTextParts[0]))
        return format_datetime(date, include_time=include_time, include_ms=include_ms)
    elif dateTextParts[1].lower() in ["day", "days", "d"]:
        date = datetime.datetime.now() - relativedelta(days=int(dateTextParts[0]))
        return format_datetime(date, include_time=include_time, include_ms=include_ms)
    elif dateTextParts[1].lower() in ["wk", "wks", "week", "weeks", "w"]:
        date = datetime.datetime.now() - relativedelta(weeks=int(dateTextParts[0]))
        return format_datetime(date, include_time=include_time, include_ms=include_ms)
    elif dateTextParts[1].lower() in ["mon", "mons", "month", "months", "m"]:
        date = datetime.datetime.now() - relativedelta(months=int(dateTextParts[0]))
        return format_datetime(date, include_time=include_time, include_ms=include_ms)
    elif dateTextParts[1].lower() in ["yrs", "yr", "years", "year", "y"]:
        date = datetime.datetime.now() - relativedelta(years=int(dateTextParts[0]))
        return format_datetime(date, include_time=include_time, include_ms=include_ms)
    else:
        raise Exception(f"Invalid date text: {past_date_text}")


def datetime_to_text(dt, also_time: bool = True, also_seconds: bool = False) -> str:
    """
    Formats the timedate obj to a string

    @param (timedate) td, timedate obj
    @param (bool) also_time = False, should the time be added
    @param (bool) also_seconds = False, if there's time should there also be seconds
    @return (string) timeDateText
    """
    timeDateFormat = "{:%d.%m.%Y}"
    if also_time:
        timeDateFormat = "{:%d.%m.%Y %H:%M}"
        if also_seconds:
            timeDateFormat = "{:%d.%m.%Y %H:%M:%S}"
    return timeDateFormat.format(dt)


def datetime_to_days_hours_minutes(td):
    """
    Returns formatted time delta obj
    http://stackoverflow.com/a/2119512
    """
    days = td.days
    remainingSeconds = td.total_seconds() - (days * 24 * 60 * 60)
    hours = int(remainingSeconds / 3600)
    minutes = int(remainingSeconds / 60) % 60
    return days, hours, minutes
