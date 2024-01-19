from rest_framework import serializers
from .models import Product, Comment, Cart, CartItem, Order, OrderItem

DOLLRS_TO_RIALS = 450000


class ProductSerializer(serializers.ModelSerializer):
    price_rials = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='api:product-detail')

    class Meta:
        model = Product
        fields = ['name', 'description', 'inventory', 'unit_price', 'price_rials', 'url', 'category']

    def get_price_rials(self, product):
        return int(product.unit_price * DOLLRS_TO_RIALS)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class AddCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_pk = self.context.get('cart_pk')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(cart_id=cart_pk, product_id=product.id)
            cart_item.quatity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_pk, **validated_data)

        self.instance = cart_item

        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body']

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'status', 'datetime_created', 'items']