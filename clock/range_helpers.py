import datetime
from typing import Optional

from pytz import timezone
from psycopg2.extras import DateTimeTZRange
from django.utils.timezone import now
from django.conf import settings


def default_time_range() -> DateTimeTZRange:
    """
    Function default value for date range, defaults to [now(), None)
    :return: Open ended date range beginning from now
    """
    return DateTimeTZRange(lower=now(), upper=None)


def format_time_range(
        time_range: DateTimeTZRange,
        time_format='%d/%m/%Y %H:%M') -> str:
    start_time_str = time_range.lower.strftime(time_format)
    end_time_str = time_range.upper.strftime(time_format) if time_range.upper else "Now"

    return f'{start_time_str} - {end_time_str}'


def to_object(
        date: datetime.datetime,
        time: datetime.time) -> datetime.datetime:
    naive_time = datetime.datetime.combine(date, time)
    return timezone(settings.TIME_ZONE).localize(naive_time)


def to_local_time(date: datetime.datetime) -> Optional[datetime.datetime]:
    return date.astimezone(timezone(settings.TIME_ZONE)) if date else None