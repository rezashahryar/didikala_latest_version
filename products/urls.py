from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('category/<slug:slug>/', views.CategoryObjectsView.as_view(), name='category_objects_view'),
    path('subCat/<slug:slug>/', views.SubCategoryObjectsView.as_view(), name='sub_category_objects_view'),
    path('detail/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('filter/', views.product_filter, name='product_filter'),
    path('question/<int:pk>/', views.question, name='question'),
    path('answer/<int:pk>/<int:qpk>', views.answer, name='answer'),
    path('add/interest-product/<int:pk>/', views.add_interest_product, name='add_interest_product'),
    path('delete/interest-product/<int:pk>/', views.delete_interest_product, name='delete_interest_product'),
]