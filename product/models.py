from uuid import uuid4

from django.db import models
from django.db.models.fields import Field

from common.models import TimeStampedModel
from django.db.models import Lookup


class Category(TimeStampedModel):
    name = models.CharField(max_length=31)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=31)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    gid = models.UUIDField(default=uuid4)
    stock_in_date = models.DateTimeField()
    stock_out_date = models.DateTimeField(null=True)
