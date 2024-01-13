from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TestAuth(APITestCase):
    def setUp(self) -> None:
        self.signup_url = reverse("user-registration")
        self.login_url = reverse("login-api")
        self.signup_data = {
            "username": "test_user_01",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@test.com",
            "password": "cB23ep$",
        }

        self.login_data = {
            "username": "test_user_01",
            "password": "cB23ep$",
        }

        return super().setUp()

    def test_01_signup(self):
        resp = self.client.post(self.signup_url, self.signup_data)
        response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response["username"], self.signup_data["username"])

    def test_02_login(self):
        resp = self.client.post(self.signup_url, self.signup_data)
        response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(self.login_url, self.login_data)
        response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(response["username"], self.signup_data["username"])
        self.assertIn("id", response)
        self.assertIn("access", response)
        self.assertIn("refresh", response)
