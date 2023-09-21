from django.shortcuts import render
from . models import Product, Cart, Category, CartItem
from . serializers import CategorySerializer, ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view()
def all_category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def all_product(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)