from django.db import models
from uuid import uuid4
from django.conf import settings
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title


class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    description = models.TextField()
    inventory = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.ManyToManyField(Discount, blank=True, related_name='products')

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.email}'


class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID, 'Paid'),
        (ORDER_STATUS_UNPAID, 'Unpaid'),
        (ORDER_STATUS_CANCELED, 'Canceled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=5, choices=ORDER_STATUS)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = [['order', 'product']]


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=5, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-datetime_created',)


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
