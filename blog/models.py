from django.db import models
from django.utils import timezone
from core.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published_date__lte=timezone.now(), status=True).order_by('-published_date')


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='blog/image/%Y/%m/%d/', default='04.jpg')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='blogs')
    tag = models.ManyToManyField(Tag, null=True, related_name='blogs')
    slug = models.SlugField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)

    published_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)

    counted_views = models.IntegerField(default=0)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = BlogManager()

    def __str__(self):
        return self.title
    