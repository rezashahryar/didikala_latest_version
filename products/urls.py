from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('category/<slug:slug>/', views.CategoryObjectsView.as_view(), name='category_objects_view'),
    path('subCat/<slug:slug>/', views.SubCategoryObjectsView.as_view(), name='sub_category_objects_view'),
    path('detail/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
]