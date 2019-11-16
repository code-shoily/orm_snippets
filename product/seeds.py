import datetime

from hypothesis import strategies

from .models import Product, Category, ProductItem


def create_categories():
    categories = [
        'Smart Phone',
        'Nostalgia',
        'Phablet',
        'Tablet',
        'Smart Watch'
    ]

    for category in categories:
        Category.objects.create(name=category, description=category)


def create_products():
    phones = [
        ('iPhone 10', 'Smart Phone', 1200),
        ('Samsung Galaxy S9', 'Smart Phone', 900),
        ('Moto Razr', 'Nostalgia', 600),
        ('Nokia 6110', 'Nostalgia', 200),
        ('Samsung Galaxy Note 10', 'Phablet', 1300),
        ('Samsung Tab 3', 'Tablet', 500),
        ('Moto 360', 'Smart Watch', 600),
        ('Pixel 2', 'Smart Phone', 900),
        ('Pixel 3', 'Smart Phone', 1000),
        ('Samsung Gear', 'Smart Watch', 400),
        ('Apple Watch', 'Smart Watch', 800),
        ('Moto G2 Play', 'Smart Phone', 400)
    ]

    for (phone, category, price) in phones:
        category = Category.objects.get(name=category)
        Product.objects.create(
            name=phone,
            price=price,
            category=category
        )


def create_product_item():
    frequency = strategies.sampled_from([100, 150, 200])
    stock_in_date = strategies.datetimes(min_value=datetime.datetime(2018, 1, 1, 0, 0, 0),
                                         max_value=datetime.datetime.now())
    for product in Product.objects.iterator():
        for i in range(frequency.example()):
            ProductItem.objects.create(
                product=product,
                stock_in_date=stock_in_date.example()
            )
