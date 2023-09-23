from django_filters.rest_framework import FilterSet
from . models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'price' : ['gt', 'lt']
        }


# class ProductFilter(filters.FilterSet):
#     min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
#     max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

#     class Meta:
#         model = Product
#         fields = ['category', 'in_stock']