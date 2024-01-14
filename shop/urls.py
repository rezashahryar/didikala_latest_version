from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('coupon/', views.coupon_apply_view, name='coupon_apply'),
    path('add/<int:pk>/', views.CartAddView.as_view(), name='cart_add'),
    path('delete/<str:id>/', views.CartDeleteView.as_view(), name='cart_delete'),
    path('delete/product/<str:id>/', views.CartDeleteViewFromHomePage.as_view(), name='cart_delete_from_home'),
    path('order/', views.order_create_view, name='order_create'),
    # path('process/', views.payment_process, name='payment_process'),
    # path('callback/', views.payment_call_back_view, name='payment_callback'),
    path('process/', views.payment_process_sandbox, name='payment_process'),
    path('callback/', views.payment_call_back_sandbox_view, name='payment_callback'),
]