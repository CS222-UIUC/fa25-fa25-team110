from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import UserProfile


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.user_data = {
            "username": "student1",
            "email": "student@example.com",
            "password": "test123",
            "user_type": "student"
        }

    def test_register_user(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(User.objects.filter(username="student1").exists())
        profile = UserProfile.objects.get(user__username="student1")
        self.assertEqual(profile.user_type, "student")

    def test_register_duplicate_user(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 400)

    def test_login_valid_user(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, {
            "username": "student1",
            "password": "test123"
        }, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("username", res.json())

    def test_login_invalid_user(self):
        res = self.client.post(self.login_url, {
            "username": "wrong",
            "password": "wrong"
        }, format="json")
        self.assertEqual(res.status_code, 401)
