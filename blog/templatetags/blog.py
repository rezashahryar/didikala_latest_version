from django import template
from blog.models import Category, Blog, Tag

register = template.Library()


@register.inclusion_tag('includes/blog_category_side_bar.html')
def category_side_bar():
    category = Category.objects.all()
    return {'categories': category}


@register.inclusion_tag('includes/blog_tag_side_bar.html')
def tag_side_bar():
    tag = Tag.objects.all()
    return {'tags': tag}


@register.inclusion_tag('includes/blog_latest_posts.html')
def latest_blog():
    blogs = Blog.published.all()[:4]
    return {'blogs': blogs}