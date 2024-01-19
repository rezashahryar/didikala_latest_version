from django.contrib import admin
from . import models
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = ('order', 'product', 'quantity', 'price')
    extra = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'datetime_created', 'is_paid')

    inlines = [
        OrderItemInline
    ]


admin.site.register(models.Coupon)
admin.site.register(models.Address)
