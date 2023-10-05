from django.shortcuts import get_object_or_404, render
from core.filters import ProductFilter
from core.pagination import DefaultPagination
from . models import Product, Cart, Category, CartItem, Order, OrderItem
from . serializers import CartItemSerializer, CategorySerializer, ProductSerializer, CartSerializer, AddItemToCartSerializer, UpdateCartItemSerializer, UpdateOrderSerializer, UserSerializer, OrderSerializer, CreateOrderSerializer
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import MethodNotAllowed
from django.db.models import Count
from django.contrib.auth import get_user_model
# Create your views here

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(products_count=Count('products')).all()    
    queryset = queryset.order_by('id')
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
    queryset = Product.objects.order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['category__title', 'name']
    filterset_class = ProductFilter  
    pagination_class = DefaultPagination
    ordering_fields = ['category', 'name']

class CartViewSet(CreateModelMixin, RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):  
    http_method_names =  ['get', 'post', 'patch', 'delete']  
    def get_queryset(self):
        queryset = CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])
        return queryset
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddItemToCartSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer


class UserViewSet(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin ,GenericViewSet):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET','PUT'])
    def me(self, request):
        user = get_user_model()
        user = user.objects.get(id=request.user.id)
        serializer = UserSerializer(user) 
        return Response(serializer.data)
    


class OrderViewSet(ModelViewSet):

    http_method_names = ['get','post','patch','delete','head']

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        new_order = serializer.save()
        serializer = OrderSerializer(new_order)
        return Response(serializer.data)

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Order.objects.filter(customer = user_id)
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]