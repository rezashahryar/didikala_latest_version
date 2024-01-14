from django.db import models
from django.utils import timezone
from core.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify


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
        return super().get_queryset().filter(published_date__lte=timezone.now(),
                                             status=Blog.BLOG_STATUS_PUBLISHED).order_by('-published_date')


class Blog(models.Model):
    BLOG_STATUS_PUBLISHED = 'p'
    BLOG_STATUS_DRAFT = 'd'

    BLOG_STATUS = [
        (BLOG_STATUS_DRAFT, 'Draft'),
        (BLOG_STATUS_PUBLISHED, 'Published')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='blog/image/%Y/%m/%d/', default='04.jpg')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='blogs')
    tag = models.ManyToManyField(Tag, related_name='blogs')
    slug = models.SlugField(null=True, blank=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)

    published_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=BLOG_STATUS, default=BLOG_STATUS_DRAFT)

    counted_views = models.IntegerField(default=0)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = BlogManager()

    class Meta:
        ordering = ('-published_date',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail_view', kwargs={'slug': self.slug})

    def get_category_objects(self):
        return reverse('blog:category_objects', kwargs={'cat_name': self.category})


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    subject = models.CharField(max_length=300, null=True)
    content = models.TextField(null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self):
        return f'blog: {self.blog.title}  content: {self.content[:15]}'


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')

    datetime_created = models.DateTimeField(auto_now_add=True)


class DisLike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dislikes')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='dislikes')

    datetime_created = models.DateTimeField(auto_now_add=True)
