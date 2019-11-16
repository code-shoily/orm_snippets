from django.db.models.functions import ExtractMonth
from django.db.models.aggregates import Avg, Sum

from .models import ProductItem


def purchases_by_month():
    return ProductItem.objects\
        .annotate(month=ExtractMonth("stock_in_date"))\
        .values("month")\
        .annotate(sales=Avg("product__price"))


def total_sale():
    return ProductItem.objects\
        .select_related("product")\
        .aggregate(total=Sum('product__price'))
