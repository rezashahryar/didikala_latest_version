from django.shortcuts import get_object_or_404
from django.views import generic
from .models import ProductCategory, SubProductCategory, Product
from django.contrib.auth.models import User


# Create your views here.


class CategoryObjectsView(generic.ListView):
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        cat = get_object_or_404(ProductCategory, slug=slug)
        return cat.products.filter(available=True)


class SubCategoryObjectsView(generic.ListView):
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        sub_cat = get_object_or_404(SubProductCategory, slug=slug)
        return sub_cat.products.filter(available=True)


class ProductDetail(generic.DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product.objects.prefetch_related('property'), slug=slug)
        # product.counted_views += 1
        # product.save()
        return product