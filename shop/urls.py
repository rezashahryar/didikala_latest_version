from django.urls import path
from . import views
from .forms import AddressForm, OrderForm
from .views import FORMS

app_name = 'shop'
urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('coupon/', views.coupon_apply_view, name='coupon_apply'),
    path('add/<int:pk>/', views.CartAddView.as_view(), name='cart_add'),
    path('delete/<str:id>/', views.CartDeleteView.as_view(), name='cart_delete'),
    path('delete/product/<str:id>/', views.CartDeleteViewFromHomePage.as_view(), name='cart_delete_from_home'),
    path('information-order/', views.information_order, name='information_order_view'),
    path('payment-page/', views.payment_page, name='payment_page'),
    path('add-address/', views.add_new_address, name='add_address_view'),
    path('edit-address/<int:pk>/', views.EditAddressView.as_view(), name='edit_address_view'),
    path('delete/address/<int:pk>/', views.delete_address, name='delete_address'),
    path('process/', views.payment_process, name='payment_process'),
    # path('test/', views.ContactWizard.as_view(FORMS), name="forms"),
    # path('callback/', views.payment_call_back_view, name='payment_callback'),
    # path('process/', views.payment_process_sandbox, name='payment_process'),
    # path('callback/', views.payment_call_back_sandbox_view, name='payment_callback'),
    # path('delete/address/<int:pk>/', views.delete_address, name='delete_address'),
]