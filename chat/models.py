from django.db import models
from django.db.models import F, When, Case


class MessageManager(models.Manager):
    def latest_distinct(self):
        return super().get_queryset().annotate(
            user_1=Case(
                When(sender__gt=F('recipient'), then=F('recipient')),
                default=F('sender')
            ),
            user_2=Case(
                When(sender__gt=F('recipient'), then=F('sender')),
                default=F('recipient')
            )
        ).order_by('user_1', 'user_2', '-when').distinct('user_1', 'user_2')


class Message(models.Model):
    when = models.DateTimeField(auto_now=True, db_index=True)
    sender = models.CharField(max_length=127)
    recipient = models.CharField(max_length=127)

    objects = MessageManager()

    def __str__(self):
        return f'[{self.when.ctime()}] {self.sender} -> {self.recipient}'
