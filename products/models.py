from django.conf import settings
from django.db import models
from django.urls import reverse
from random import uniform
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import format_html
# Create your models here.


class Color(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ProductProperties(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    properties = models.ManyToManyField(ProductProperties)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    picture = models.ImageField(upload_to='category_pictures')

    def get_absolute_url(self):
        return reverse('products:category_objects_view', args=[self.slug])

    def __str__(self):
        return self.title


class SubProductCategory(models.Model):
    main_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    parent = models.ForeignKey('self', related_name='sub_children', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:sub_category_objects_view', args=[self.slug])


def random_number():
    num = int(uniform(1000, 100000))
    return str(num)


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True).order_by('-created_date')


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(SubProductCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True)
    product_code = models.CharField(max_length=8, default=random_number)
    available = models.BooleanField(default=True)

    cover = models.ImageField(upload_to='products/covers')
    img_one = models.ImageField(upload_to='products/img_one', null=True, blank=True)
    img_two = models.ImageField(upload_to='products/img_two', null=True, blank=True)
    img_three = models.ImageField(upload_to='products/img_three', null=True, blank=True)

    color = models.ManyToManyField(Color, related_name='colors', null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brands', null=True, blank=True)

    discount = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    price = models.IntegerField()
    description = models.TextField()
    counted_views = models.IntegerField(default=0)

    sales_number = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    list = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    @property
    def get_discount(self):
        if self.discount > 0:
            return True
        return None

    def get_price_after_discount(self):
        price = int(self.price * self.discount / 100)
        return price


class SetProductProperty(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='property')
    property = models.ForeignKey(ProductProperties, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f'property {self.property} for {self.product.title} with value {self.value}'


class Question(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='answers', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return format_html(
            '<span>{}</span><b> for </b><span>{}</span> product', self.user, self.product
        )