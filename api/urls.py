from django.urls import path, include
from . import views
from rest_framework_nested import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)




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
    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # end
]

