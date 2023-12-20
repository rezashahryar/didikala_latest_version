from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Blog, Category, Tag


# Create your views here.


class BlogListView(generic.ListView):
    queryset = Blog.published.all()
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 12


class BlogDetailView(generic.DetailView):
    context_object_name = 'blog'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Blog, slug=slug, status=True)


class CategoryObjectsView(generic.ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 12

    def get_queryset(self):
        cat_name = self.kwargs.get('cat_name')
        category = get_object_or_404(Category, name=cat_name)
        return category.blogs.filter(status=True)


class TagObjectsView(generic.ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 12

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        tag = get_object_or_404(Tag, name=tag_name)
        return tag.blogs.filter(status=True)