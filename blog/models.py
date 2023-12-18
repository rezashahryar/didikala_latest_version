from django.db import models
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)


class BlogManager(models.Manager):
    def published(self):
        return self.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date')


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='blog/image/%Y/%m/%d/')

    published_date = models.DateTimeField()
    status = models.BooleanField(default=False)

    counted_views = models.IntegerField(default=0)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = BlogManager()

    def __str__(self):
        return self.title
    