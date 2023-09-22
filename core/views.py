from django.shortcuts import render
from . models import Product, Cart, Category, CartItem
from . serializers import CategorySerializer, ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count

# Create your views her

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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