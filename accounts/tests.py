from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTestCase(TestCase):
    def test_create_student_profile(self):
        """Test creating a student user profile"""
        user = User.objects.create_user(username="student1", password="test123")
        profile = UserProfile.objects.create(user=user, user_type="student")
        self.assertEqual(profile.user_type, "student")
        self.assertEqual(profile.user.username, "student1")

    def test_create_professor_profile(self):
        """Test creating a professor user profile"""
        user = User.objects.create_user(username="prof1", password="test123")
        profile = UserProfile.objects.create(user=user, user_type="professor")
        self.assertEqual(profile.user_type, "professor")
        self.assertEqual(profile.user.username, "prof1")

    def test_default_user_type(self):
        """Test that default user type is student"""
        user = User.objects.create_user(username="default1", password="test123")
        profile = UserProfile.objects.create(user=user)
        self.assertEqual(profile.user_type, "student")

    def test_profile_string_representation(self):
        """Test string representation of profile"""
        user = User.objects.create_user(username="prof2", password="test123")
        profile = UserProfile.objects.create(user=user, user_type="professor")
        self.assertEqual(str(profile), "prof2 - professor")

    def test_student_profile_string(self):
        """Test student profile string"""
        user = User.objects.create_user(username="student2", password="test123")
        profile = UserProfile.objects.create(user=user, user_type="student")
        self.assertEqual(str(profile), "student2 - student")


class AuthAPITestCase(TestCase):
    def test_register_student(self):
        """Test student registration endpoint"""
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "teststudent",
                "email": "student@example.com",
                "password": "test123",
                "user_type": "student",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="teststudent").exists())

    def test_register_professor(self):
        """Test professor registration endpoint"""
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "testprof",
                "email": "prof@example.com",
                "password": "test123",
                "user_type": "professor",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.get(user__username="testprof")
        self.assertEqual(profile.user_type, "professor")

    def test_register_duplicate_username(self):
        """Test that duplicate usernames are rejected"""
        self.client.post(
            "/api/auth/register/",
            {
                "username": "duplicate",
                "email": "test1@example.com",
                "password": "test123",
                "user_type": "student",
            },
            content_type="application/json",
        )

        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "duplicate",
                "email": "test2@example.com",
                "password": "test123",
                "user_type": "student",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        """Test successful login"""
        user = User.objects.create_user(username="logintest", password="test123")
        UserProfile.objects.create(user=user, user_type="student")

        response = self.client.post(
            "/api/auth/login/",
            {"username": "logintest", "password": "test123"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.json())
        self.assertIn("user_type", response.json())

    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        user = User.objects.create_user(username="testuser", password="correct123")
        UserProfile.objects.create(user=user, user_type="student")

        response = self.client.post(
            "/api/auth/login/",
            {"username": "testuser", "password": "wrong123"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
