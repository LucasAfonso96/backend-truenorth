from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from calculator.models import CustomUser, Operation
import json


class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        url = reverse('register')
        data = {
            "email": "newuser@example.com",
            "password": "newuserpassword",
        }
        body = json.dumps(data) 
        response = self.client.post(url, content_type='application/json', data=body)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        url = reverse('login')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }
        body = json.dumps(data) 
        response = self.client.post(url, content_type='application/json', data=body)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    # Add more API tests for other endpoints

class OperationListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('operations')

    def test_get_operation_list(self):
        operation1 = Operation.objects.create(type='addition', cost=5.0)
        operation2 = Operation.objects.create(type='subtraction', cost=3.0)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['type'], operation1.type)
        self.assertEqual(response.data[0]['cost'], operation1.cost)
        self.assertEqual(response.data[1]['type'], operation2.type)
        self.assertEqual(response.data[1]['cost'], operation2.cost)
