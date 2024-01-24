from django.db import models
from django.utils import timezone
from core.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model):
    name = models.CharField(_('نام'), max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(_('نام'), max_length=100)

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
        (BLOG_STATUS_DRAFT, _('Draft')),
        (BLOG_STATUS_PUBLISHED, _('Published'))
    ]
    title = models.CharField(_('عنوان'), max_length=255)
    description = RichTextField(verbose_name=_('توضیحات'))
    image = models.ImageField(_('عکس'), upload_to='blog/image/%Y/%m/%d/', default='04.jpg')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='blogs', verbose_name=_('دسته بندی'))
    tag = models.ManyToManyField(Tag, related_name='blogs', null=True, verbose_name=_('بر چسب'))
    slug = models.SlugField(_('مسیر یو ار ال'), null=True, blank=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True, verbose_name=_('نویسنده'))

    published_date = models.DateTimeField(_('تاریخ انتشار'), null=True, blank=True)
    status = models.CharField(_('وضعیت انتشار'), max_length=10, choices=BLOG_STATUS, default=BLOG_STATUS_DRAFT)

    counted_views = models.IntegerField(_('تعداد بازدید'), default=0)

    datetime_created = models.DateTimeField(_('datetime_created'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('datetime_updated'), auto_now=True)

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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name=_('کاربر'))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name=_('مقاله'))
    subject = models.CharField(_('عنوان'), max_length=300, null=True)
    content = models.TextField(_('محتوا'), null=True)

    datetime_created = models.DateTimeField(_('datetime_created'), auto_now_add=True)

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self):
        return f'blog: {self.blog.title}  content: {self.content[:15]}'


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes', verbose_name=_('کاربر'))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes', verbose_name=_('مقاله'))

    datetime_created = models.DateTimeField(_('datetime_created'), auto_now_add=True)


class DisLike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dislikes', verbose_name=_('کاربر'))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='dislikes', verbose_name=_('مقاله'))

    datetime_created = models.DateTimeField(_('datetime_created'), auto_now_add=True)
