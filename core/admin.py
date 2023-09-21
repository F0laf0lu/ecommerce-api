from typing import Any
from django.contrib import admin
from django.urls import reverse
from . models import Category, Product, Cart, CartItem
from django.db.models import Count
from django.utils.html import format_html
# Register your models here.


@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_total']
    search_fields = ['title']
    @admin.display(ordering='products_total')
    def products_total(self, category):
        url = reverse('admin:core_product_changelist') + '?' + f'category__id={category.pk}'
        return format_html (f'<a href="{url}">{category.products_total}<a>')
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_total = Count('product'))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    list_display = ['name', 'category' , 'price']
    list_per_page = 15
    list_editable = ['price']
    search_fields = ['name', 'category__title']

admin.site.register(Cart)
admin.site.register(CartItem)