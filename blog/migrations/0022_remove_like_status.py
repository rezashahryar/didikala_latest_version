# Generated by Django 4.2.7 on 2024-01-14 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_like_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='status',
        ),
    ]