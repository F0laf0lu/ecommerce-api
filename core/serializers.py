from rest_framework import serializers
from core.models import Category, Product, Cart, CartItem


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
    # product = serializers.CharField(source='product.name')
    product = SimpleProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at']
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cart = Cart.objects.create(**validated_data)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)

        return cart


