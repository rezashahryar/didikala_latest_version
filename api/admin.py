from django.contrib import admin
from . import models
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<3', 'High'),
            ('3<=', 'Medium'),
            ('>10', 'Ok')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<3':
            return queryset.filter(inventory__lt=3)
        if self.value() == '3<=':
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == '>10':
            return queryset.filter(inventory__gt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime_created'
    list_display = ['name', 'inventory', 'unit_price', 'inventory_status', 'product_category', 'num_of_comments']
    list_per_page = 50
    list_editable = ['unit_price']
    list_select_related = ['category']
    list_filter = ['datetime_created', InventoryFilter]
    search_fields = ['name']
    actions = ['clear_inventory']
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comments').annotate(comments_count=Count('comments'))

    def num_of_comments(self, product):
        url = (
            reverse('admin:api_comment_changelist')
             + '?'
            + urlencode({
            'product__id': product.id
        })
        )
        return format_html(
            '<a href="{}">{}</a>', url, product.comments_count
        )
        # return product.comments_count

    @admin.action(description='clear_inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(request, f'{update_count} of products inventories cleared to zero')

    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        if product.inventory > 50:
            return 'High'
        return 'Medium'

    @admin.display(ordering='category__title', description='category')
    def product_category(self, product):
        return product.category.title


class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    fields = ['product', 'quantity']
    extra = 1
    min_num = 1

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'num_of_items', 'status']
    list_editable = ['status']
    list_per_page = 50
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items').annotate(items_count=Count('items'))

    @admin.display(ordering='items_count')
    def num_of_items(self, order):
        return order.items_count


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'status']
    list_editable = ['status']
    list_per_page = 20
    autocomplete_fields = ['product']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_per_page = 100
    search_fields = ['fist_name', 'last_name']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    autocomplete_fields = ['product']


class CartItemTabular(admin.TabularInline):
    model = models.CartItem
    fields = ['cart', 'product', 'quantity']
    extra = 1
    min_num = 1


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    inlines = [CartItemTabular]




admin.site.register(models.Category)
admin.site.register(models.CartItem)
admin.site.register(models.Discount)
admin.site.register(models.Address)