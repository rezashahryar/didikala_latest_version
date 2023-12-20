# Generated by Django 4.2.7 on 2023-12-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_tag_blog_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='tag',
        ),
        migrations.AddField(
            model_name='blog',
            name='tag',
            field=models.ManyToManyField(null=True, related_name='blogs', to='blog.tag'),
        ),
    ]
