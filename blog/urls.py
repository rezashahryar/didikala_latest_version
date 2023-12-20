from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('list/', views.BlogListView.as_view(), name='blog_list_view'),
    path('detail/<str:slug>/', views.BlogDetailView.as_view(), name='blog_detail_view'),
    path('category/<str:cat_name>/', views.CategoryObjectsView.as_view(), name='category_objects'),
    path('tag/<str:tag_name>/', views.TagObjectsView.as_view(), name='Tag_objects'),
]
