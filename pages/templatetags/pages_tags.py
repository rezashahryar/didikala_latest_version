from django import template
from products.models import ProductCategory, Product
from django.db.models import Count

register = template.Library()


@register.inclusion_tag("includes/product_category_objects.html")
def product_categories():
    categories = ProductCategory.objects.prefetch_related('products').annotate(products_count=Count('products'))
    return {'categories': categories}
