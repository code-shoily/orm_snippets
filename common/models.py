from django.db import models


class TimeStampedModel(models.Model):
    """
    A timestamped model is a model that has creation and modification timestamps. Any models
    inheriting this would automatically get `created_at` and `updated_at` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True