from django.contrib import admin
from . models import Product, ProductCategory, ProductProperties, SubProductCategory, SetProductProperty, Brand, Color, Question
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_code', 'available', 'price', 'category', 'discount')
    list_editable = ['available', 'discount']


admin.site.register(ProductCategory)
admin.site.register(SubProductCategory)
admin.site.register(ProductProperties)
admin.site.register(SetProductProperty)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Question)