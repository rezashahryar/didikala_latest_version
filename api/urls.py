from django.urls import path, include
from . import views
from rest_framework_nested import routers

app_name = 'api'


router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')
products_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_routers.register('comments', views.CommentViewSet, basename='product_comments')

router.register('orders', views.OrderViewSet, basename='order')

router.register('carts', views.CartViewSet, basename='cart')
cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart_items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_routers.urls)),
    path('', include(cart_items_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

