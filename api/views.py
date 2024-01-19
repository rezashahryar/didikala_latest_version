from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from .models import Product, Comment, Cart, CartItem, OrderItem, Order
from .serializers import (ProductSerializer, CommentSerializer, CartSerializer, CartItemSerializer,
                          AddCartItemSerializer, UpdateCartItemSerializer,
                          OrderSerializer, OrderItemSerializer,
                          )
from .filters import ProductFilter
from .paginations import ProductPagination
from django.db.models import Prefetch

# Create your views here.


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product')
            )
        ).select_related('customer').all()


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        cart_pk = self.kwargs.get('cart_pk')
        return CartItem.objects.select_related('product').filter(cart__id=cart_pk)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        cart_pk = self.kwargs.get('cart_pk')
        return {'cart_pk': cart_pk}


class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    # lookup_value_regex = '[0-9a-f]{32}'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    pagination_class = ProductPagination

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk)

    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}
