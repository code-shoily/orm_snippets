from django.contrib import admin
from django.contrib.postgres.aggregates import StringAgg

from django.db.models import Count, Subquery, OuterRef, Avg
from django.utils.safestring import mark_safe

from .models import ProductItem, Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "name", "number_of_products", "product_names", "average_price"
    ordering = "name",
    search_fields = "name", "description",

    def number_of_products(self, obj):
        return obj.total

    number_of_products.admin_order_field = "total"

    def product_names(self, obj):
        html = "<li>{}</li>"
        elems = "".join([html.format(i) for i in sorted(obj.product_names.split("||")[:3])])
        print("\n\n\n" + elems + "\n\n\n")
        return mark_safe(f"<ul>{elems}</ul>")

    product_names.admin_order_field = "product_names"

    def average_price(self, obj):
        res = "<div style='text-align:right; width=100%'>CA${:.2f}</div>".format(obj.average_price)
        return mark_safe(res)

    average_price.admin_order_field = "average_price"

    def get_queryset(self, request):
        return super().get_queryset(self).annotate(
            total=Subquery(Product.objects.filter(category=OuterRef("pk")).values("category").annotate(
                total=Count("pk")).values("total")),
            product_names=Subquery(
                Product.objects.filter(
                    category=OuterRef("pk")).values("category").annotate(names=StringAgg("name", "||")).values("names")
            ),
            average_price=Subquery(
                Product.objects.filter(
                    category=OuterRef("pk")).values("category").annotate(avg_price=Avg("price")).values("avg_price")
            ),
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ["product", "category", "gid", "stock_in_date", "stock_out_date"]

    def category(self, obj):
        return obj.product.category

