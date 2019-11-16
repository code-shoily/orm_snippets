from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.postgres.fields import CITextField, CICharField, JSONField
from phonenumber_field.modelfields import PhoneNumberField

from common.models import TimeStampedModel


class Customer(TimeStampedModel):
    name = models.CharField(max_length=127)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    address = CITextField(blank=True)
    bio = CICharField(blank=True, max_length=31)
    preferences = JSONField(null=True)

    def __str__(self):
        return self.name