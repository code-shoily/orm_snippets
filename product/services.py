from django.db.models.functions import ExtractMonth
from django.db.models.aggregates import Avg, Sum
from django.db.models import Window, Q, F
from django.contrib.postgres.search import SearchVector, TrigramSimilarity

from .models import ProductItem, Product


def purchases_by_month():
    return ProductItem.objects\
        .annotate(month=ExtractMonth("stock_in_date"))\
        .values("month")\
        .annotate(sales=Avg("product__price"))


def total_sale():
    return ProductItem.objects\
        .select_related("product")\
        .aggregate(total=Sum('product__price'))


def average_price():
    return Product.objects.annotate(
        average_by_category=Window(
            expression=Avg('price'),
            partition_by=[F('category')],
            order_by=F('category').asc()
        )
    ).values('name', 'category__name', 'average_by_category')


def find_in_category_or_product(query):
    return Product.objects.select_related('category').annotate(
        category_name=F('category__name'),
    ).annotate(
        search=SearchVector('name') + SearchVector('category_name')
    ).filter(search=query)


def fuzzy_name_finder(term, model=Product):
    return model.objects.annotate(
        similarity=TrigramSimilarity('name', term)
    ).filter(similarity__gt=0.1).order_by('-similarity')
