# Generated by Django 4.2.7 on 2024-01-24 18:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_brand_title_alter_color_title_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0003_alter_address_post_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.TextField(verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=100, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='address',
            name='full_name',
            field=models.CharField(max_length=500, verbose_name='نام و نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='address',
            name='mobile_number',
            field=models.CharField(max_length=15, verbose_name='شماره تلفن'),
        ),
        migrations.AlterField(
            model_name='address',
            name='post_code',
            field=models.CharField(max_length=10, verbose_name='کد پستی'),
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.CharField(max_length=100, verbose_name='استان'),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=50, unique=True, verbose_name='کد'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(verbose_name='از تاریخ'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(verbose_name='تا تاریخ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=700, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='order',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='datetime_created'),
        ),
        migrations.AlterField(
            model_name='order',
            name='datetime_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='datetime_modified'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='وضعیت پرداخت'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_code',
            field=models.CharField(blank=True, default=shop.models.order_code, max_length=50, null=True, verbose_name='کد سفارش'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_notes',
            field=models.CharField(blank=True, max_length=700, verbose_name='یادداشت'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=15, verbose_name='شماره همراه'),
        ),
        migrations.AlterField(
            model_name='order',
            name='post_code',
            field=models.CharField(blank=True, max_length=20, verbose_name='کد پستی'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price_order',
            field=models.IntegerField(blank=True, null=True, verbose_name='مبلغ کل'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order', verbose_name='سفارش'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.PositiveIntegerField(verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='products.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='تعداد'),
        ),
    ]