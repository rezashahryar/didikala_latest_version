from django.shortcuts import render
from django.views import generic
from .models import Blog
# Create your views here.


class BlogListView(generic.ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.objects.published()
