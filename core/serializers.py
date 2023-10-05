from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from core.models import Category, Product, Cart, CartItem, Order, OrderItem
from rest_framework import status
from django.db import transaction
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "products_count"]
    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price']

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    # product = serializers.CharField(source='product.name', read_only=True)
    product = SimpleProductSerializer()
    total = serializers.SerializerMethodField()
    def get_total(self, cartitem):
        return cartitem.quantity * cartitem.product.price
    class Meta:
        model = CartItem
        fields = ['id', 'product','quantity', 'total']
    

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id','items','cart_total']
    
    cart_total = serializers.SerializerMethodField()
    def get_cart_total(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

class AddItemToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Invalid Product ID")
        return value

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        cart_id = self.context['cart_id']
        quantity = self.validated_data['quantity']
        print(self.validated_data)
        
        try:
            cartitem = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields  = ['quantity']


user = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "unit_price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','placed_at', "payment_status", "customer", "items"]

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = user.objects.get(id=self.context['user_id'])
            new_order = Order.objects.create(customer = customer)
            cartitems = CartItem.objects.filter(cart_id=cart_id)

            order_items = [OrderItem(
                order = new_order,
                product = item.product,
                quantity = item.quantity,
                unit_price = item.product.price
            ) for item in cartitems
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(id=cart_id).delete()