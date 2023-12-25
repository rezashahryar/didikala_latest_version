from django.db import models
from django.urls import reverse
from random import uniform
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class ProductProperties(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    properties = models.ManyToManyField(ProductProperties)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
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


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(SubProductCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    product_code = models.CharField(max_length=8, default=random_number)
    available = models.BooleanField(default=True)

    cover = models.ImageField(upload_to='products/covers')
    img_one = models.ImageField(upload_to='products/img_one')
    img_two = models.ImageField(upload_to='products/img_two')
    img_three = models.ImageField(upload_to='products/img_three')

    discount = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    price = models.IntegerField()
    description = models.TextField()
    counted_views = models.IntegerField(default=0)

    sales_number = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_detail_view', args=[self.slug])


class SetProductProperty(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='property')
    property = models.ForeignKey(ProductProperties, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f'property {self.property} for {self.product.title} with value {self.value}'