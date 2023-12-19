from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Blog
# Create your views here.


class BlogListView(generic.ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.published.all()


class BlogDetailView(generic.DetailView):
    context_object_name = 'blog'
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Blog, slug=slug, status=True)
