from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_category, name='category-list'),
    path('products/', views.all_product, name='product-list'),
]
