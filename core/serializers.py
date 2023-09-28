from decimal import Decimal
from rest_framework import serializers
from core.models import Category, Product, Cart, CartItem
from rest_framework import status

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

    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')
    #     cart = Cart.objects.create(**validated_data)
    #     for item_data in items_data:
    #         CartItem.objects.create(cart=cart, **item_data)
    #     return cart


class AddItemToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Invalid Product ID")

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        cart_id = self.context['cart_id']
        quantity = self.validated_data['quantity']

        try:
            cartitem = CartItem.objects.get(cart_id=cart_id, product_id=product_id, quantity=quantity)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields  = ['quantity']
