# Generated by Django 4.2.7 on 2024-01-13 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0017_remove_like_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='blog.blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
