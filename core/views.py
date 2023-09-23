from django.shortcuts import render
from . models import Product, Cart, Category, CartItem
from . serializers import CategorySerializer, ProductSerializer, CartSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.db.models import Count

# Create your views her

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(products_count=Count('products')).all()
    serializer_class = CategorySerializer
    
    # customize retrieve method to get products in a category
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        products = Product.objects.filter(category=instance)
        product_serializer = ProductSerializer(products, many=True)
        response_data = {
            'category':self.get_serializer(instance).data,
            'products': product_serializer.data
        }
        return Response(response_data)
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
