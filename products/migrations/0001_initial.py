# Generated by Django 4.2.7 on 2023-12-14 14:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('product_code', models.CharField(default=products.models.random_number, max_length=8)),
                ('available', models.BooleanField(default=True)),
                ('cover', models.ImageField(upload_to='products/covers')),
                ('img_one', models.ImageField(upload_to='products/img_one')),
                ('img_two', models.ImageField(upload_to='products/img_two')),
                ('img_three', models.ImageField(upload_to='products/img_three')),
                ('discount', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('counted_views', models.IntegerField(default=0)),
                ('sales_number', models.PositiveIntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('picture', models.ImageField(upload_to='category_pictures')),
            ],
        ),
        migrations.CreateModel(
            name='ProductProperties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('main_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.productcategory')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_children', to='products.subproductcategory')),
            ],
        ),
        migrations.CreateModel(
            name='SetProductProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=250)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property', to='products.product')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productproperties')),
            ],
        ),
        migrations.AddField(
            model_name='productcategory',
            name='properties',
            field=models.ManyToManyField(to='products.productproperties'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.subproductcategory'),
        ),
    ]