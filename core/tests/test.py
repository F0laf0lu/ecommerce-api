import json
from django.test import TestCase
from django.urls import reverse
from core.models import Category, Product
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from datetime import datetime

# Create your tests here.
class CategoryAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category')

    def test_get_all_category(self):
        url  = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_specific_category(self):
        url  = reverse('category-detail', kwargs={'pk':self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_put_delete_not_allowed(self):
        data = {
            'title':'category',
        }
        list_url = reverse('category-list')
        detail_url = reverse('category-detail', kwargs={'pk':self.category.pk})

        post_response = self.client.post(list_url, data, content_type='application/json')
        put_response = self.client.put(detail_url, data, content_type='application/json')
        delete_response = self.client.delete(detail_url)

        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ProductAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(name='Test Product',category = self.category, price = 34.5)
        self.product_data = {
            "name": "Test Product",
            "description": "Lorem ipsum hgudk",
            "category": self.category.pk,
            "price": 20.00,
        }

    def test_get_all_products(self):
        url  = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_product(self):
        url  = reverse('product-detail', kwargs={'pk':self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_new_product(self):
        url = reverse('product-list')
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_product(self):
        url  = reverse('product-detail', kwargs={'pk':self.product.pk}) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_product(self):
        updated_data = {
            "name": "Updated Product",
            "description": "Lorem ipsum abcdefg",
            "category": self.category.pk,
            "price": 35.00,
        }
        url  = reverse('product-detail', kwargs={'pk':self.product.pk}) 
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)