from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint
router = DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('product', views.ProductViewSet)
router.register('cart', views.CartViewSet)

cart_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls))
]
