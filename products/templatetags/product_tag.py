from django import template
from products.models import Product


register = template.Library()


@register.inclusion_tag('includes/most_visited_products.html')
def most_visited_products():
    products = Product.objects.all().order_by('-counted_views')
    return {'most_visited_products': products}