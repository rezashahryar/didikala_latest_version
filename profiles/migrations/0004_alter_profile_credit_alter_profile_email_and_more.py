# Generated by Django 4.2.7 on 2024-01-24 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='credit',
            field=models.PositiveIntegerField(default=0, verbose_name='اعتبار'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='نام و نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='avatar.png', null=True, upload_to='profile_image', verbose_name='عکس'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='national_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='کد ملی'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
