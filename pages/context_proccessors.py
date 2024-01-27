from products.models import ProductCategory


def product_category(request):
    return {
        'categories': ProductCategory.objects.prefetch_related('children')
    }