from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from random import uniform
from django.conf import settings
# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


def order_code():
    result = int(uniform(10000, 99999))
    return f'DDK-{result}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    is_paid = models.BooleanField(_('is_paid'), default=False)

    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last_name'), max_length=100)
    email = models.EmailField(_('email'), )
    phone_number = models.CharField(_('phone_number'), max_length=15)
    address = models.CharField(_('address'), max_length=700)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    order_notes = models.CharField(_('order_notes'), max_length=700, blank=True)

    post_code = models.CharField(_('post_code'), max_length=20, blank=True)

    order_code = models.CharField(max_length=50, default=order_code, null=True, blank=True)

    total_price_order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self):
        return f'Order{self.id}'

    def get_total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'OrderItem {self.id} of order {self.order.id}'