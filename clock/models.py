from django.db import models
from django.db.models import F, Q, ExpressionWrapper, DurationField, Case, When, BooleanField
from django.db.models.functions import Upper, Lower, Now
# from django.contrib.postgres.
from django.contrib.postgres.fields.ranges import DateTimeRangeField
from django.utils.timezone import now
from django.conf import settings
from psycopg2.extras import DateTimeTZRange

from common.models import TimeStampedModel
from .range_helpers import default_time_range, format_time_range


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            start_time=Lower('time_range'),
            end_time=Upper('time_range'),
            is_current=Case(
                When(
                    end_time__isnull=True,
                    then=True),
                default=False,
                output_field=BooleanField()),
            duration=Case(
                When(is_current=True,
                     then=ExpressionWrapper(Now() - F('start_time'),
                                            output_field=DurationField())),
                default=ExpressionWrapper(F('end_time') - F('start_time'),
                                          output_field=DurationField()))
        )


class Event(TimeStampedModel):
    """
    An attendance event. An instance represents a users attendance status on a particular
    time range. If the time range is open ended (i.e. end-time is None), then it means the
    user is currently in the premise. No new instance can be created for a user if the user
    has an open ended time-range. In other words, a user cannot check-in without checking out
    first.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_range = DateTimeRangeField(db_index=True, default=default_time_range)
    remarks = models.TextField(blank=True)

    objects = EventManager()

    def __str__(self):
        return f'{self.user.username}: ({format_time_range(self.time_range)})'

    class Meta:
        ordering = '-time_range',
        # constraints = [
        #     ExclusionConstraint(
        #         name='exclude_overlapping_reservations',
        #         expressions=[
        #             ('time_range', RangeOperators.OVERLAPS),
        #             ('user', RangeOperators.EQUAL),
        #         ]
        #     ),
        # ]


def create_event(user, start_time=None, end_time=None) -> Event:
    return Event.objects.create(
        user=user, time_range=DateTimeTZRange(lower=start_time or now(), upper=end_time))


def update_event(pk, start_time, end_time) -> Event:
    return Event.objects.get(id=pk).update(
        time_range=DateTimeTZRange(lower=start_time, upper=end_time))