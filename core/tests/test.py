import json
from django.test import TestCase
from django.urls import reverse
from core.models import Category, Product
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime

# Create your tests here.
class CategoryAPITest(TestCase):
    def setup(self):
        self.client = APIClient()
    # Category
    def test_get_all_category(self):
        url  = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_specific_category(self):
        category = Category.objects.create(title='Test Category')
        url  = reverse('category-detail', kwargs={'pk':category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_put_delete_not_allowed(self):
        category = Category.objects.create(title='Test Category')
        data = {
            'title':'category',
        }
        list_url = reverse('category-list')
        detail_url = reverse('category-detail', kwargs={'pk':category.pk})

        post_response = self.client.post(list_url, data, content_type='application/json')
        put_response = self.client.put(detail_url, data, content_type='application/json')
        delete_response = self.client.delete(detail_url)

        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete_response.status_code, status.HTTP_20)


