from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from random import uniform
# Create your models here.


class Coupon(models.Model):
    code = models.CharField(_('کد'), max_length=50, unique=True)
    valid_from = models.DateTimeField(_('از تاریخ'))
    valid_to = models.DateTimeField(_('تا تاریخ'))
    discount = models.PositiveIntegerField(_('درصد تخفیف'), validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(_('فعال'), default=True)

    def __str__(self):
        return self.code


def order_code():
    result = int(uniform(10000, 99999))
    return f'DDK-{result}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders", verbose_name=_('کاربر'))
    is_paid = models.BooleanField(_('وضعیت پرداخت'), default=False)

    first_name = models.CharField(_('نام'), max_length=100)
    last_name = models.CharField(_('نام خانوادگی'), max_length=100)
    email = models.EmailField(verbose_name=_('ایمیل'))
    phone_number = models.CharField(_('شماره همراه'), max_length=15)
    address = models.CharField(_('آدرس'), max_length=700)

    datetime_created = models.DateTimeField(_('datetime_created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('datetime_modified'), auto_now=True)

    order_notes = models.CharField(_('یادداشت'), max_length=700, blank=True)

    post_code = models.CharField(_('کد پستی'), max_length=20, blank=True)

    order_code = models.CharField(_('کد سفارش'), max_length=50, default=order_code, null=True, blank=True)

    total_price_order = models.IntegerField(_('مبلغ کل'), null=True, blank=True)

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self):
        return f'Order{self.id}'

    def get_total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('سفارش'))
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items', verbose_name=_('محصول'))
    quantity = models.PositiveIntegerField(_('تعداد'), default=1)
    price = models.PositiveIntegerField(_('قیمت'), )

    def __str__(self):
        return f'OrderItem {self.id} of order {self.order.id}'


# class AddressManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter()


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='address', verbose_name=_('کاربر'))
    full_name = models.CharField(_('نام و نام خانوادگی'), max_length=500)
    mobile_number = models.CharField(_('شماره تلفن'), max_length=15)
    province = models.CharField(_('استان'), max_length=100)
    city = models.CharField(_('شهر'), max_length=100)
    address = models.TextField(_('آدرس'))
    post_code = models.CharField(_('کد پستی'), max_length=10)

    # get_address = AddressManager()

    def __str__(self):
        return self.address