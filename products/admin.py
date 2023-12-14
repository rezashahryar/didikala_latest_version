from django.contrib import admin
from . models import Product, ProductCategory, ProductProperties, SubProductCategory, SetProductProperty
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_code', 'available', 'price')


admin.site.register(ProductCategory)
admin.site.register(SubProductCategory)
admin.site.register(ProductProperties)
admin.site.register(SetProductProperty)