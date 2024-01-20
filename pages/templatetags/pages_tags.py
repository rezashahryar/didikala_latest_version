from django import template
from products.models import ProductCategory, Product

register = template.Library()


@register.inclusion_tag("includes/product_category_objects.html")
def product_categories():
    # global categories
    products = Product.list.select_related('category')
    categories = ProductCategory.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = products.filter(category=name).count()
    return {'categories': cat_dict}


# @register.inclusion_tag('includes/table_of_categories.html')
# def categories():
#     return {'categories_all': categories}