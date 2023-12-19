from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('list/', views.BlogListView.as_view(), name='blog_list_view'),
    path('detail/<str:slug>/', views.BlogDetailView.as_view(), name='blog_detail_view'),
]
