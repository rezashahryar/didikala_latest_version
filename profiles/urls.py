from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.profile_view, name='profile_main_page'),
    path('additional/info/', views.profile_additional_info_view, name='additional_info'),
    path('additional/info/change/', views.profile_additional_info_change_view, name='additional_info_change'),
    path('orders/', views.profile_order_list_view, name='user_orders'),
    path('order/detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/return/', views.profile_user_orders_return, name='user_orders_return'),
    path('change/information/', views.profile_edit_view, name='profile_edit'),
    path('user/comments/', views.user_comments, name='user_comments'),
    path('user/addresses/', views.user_addresses, name='user_addresses'),
    path('address/', views.add_new_address, name='add_address_view'),
    path('address/update/<int:pk>/', views.EditAddressView.as_view(), name='edit_address_view'),
    path('address/delete/<int:pk>/', views.delete_address, name='delete_address_view'),
    path('interest-product/list/', views.interest_product_list, name='interest_product_list'),
]