from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    def test_register(self):
        data={
            "username": "shakil",
            "email": "shakil@gmail.com",
            "password": "shakil",
            "password2": "shakil"
        }
        response = self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="shakil2020",password="shakil420")
    def test_login(self):
        data={
            "username":"shakil2020",
            "password":"shakil420"
        }
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_logout(self):
        self.token = Token.objects.get(user__username="shakil2020")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)