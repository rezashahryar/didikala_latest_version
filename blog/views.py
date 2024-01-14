from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from .models import Blog, Category, Tag, Like, DisLike
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

# Create your views here.


class BlogListView(generic.ListView):
    queryset = Blog.published.all()
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 12


class BlogDetailView(generic.DetailView):
    context_object_name = 'blog'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blog.published.select_related('author'), slug=slug)
        # blog.counted_views += 1
        # blog.save()
        return blog


class CategoryObjectsView(generic.ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 12

    def get_queryset(self):
        cat_name = self.kwargs.get('cat_name')
        category = get_object_or_404(Category, name=cat_name)
        return category.blogs.filter(status=Blog.BLOG_STATUS_PUBLISHED)


class TagObjectsView(generic.ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 12

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        tag = get_object_or_404(Tag, name=tag_name)
        return tag.blogs.filter(status=Blog.BLOG_STATUS_PUBLISHED)

@login_required
def like(request, slug, pk):
    try:
        like = get_object_or_404(Like, blog__slug=slug, user_id=request.user.id)
        like.delete()
    except:
        Like.objects.create(blog_id=pk, user_id=request.user.id)

    return redirect('blog:blog_detail_view', slug)

@login_required()
def dislike(request, slug, pk):
    try:
        user = request.user.id
        dislike = get_object_or_404(DisLike, blog__slug=slug, user_id=user)
        dislike.delete()

    except:
        DisLike.objects.create(blog_id=pk, user_id=request.user.id)

    return redirect('blog:blog_detail_view', slug)


def create_comment_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status=Blog.BLOG_STATUS_PUBLISHED)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.blog = blog
            new_form.user = request.user
            new_form.save()
            return redirect('blog:blog_detail_view', slug)
