from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("token")
ME_URL = reverse("user:manage")

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def set_up(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exist(self):
        payload = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_password_too_short(self):
        payload = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "tes",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        user_exist = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        create_user(
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password="testpassword",
        )

        res = self.client.post(
            TOKEN_URL,
            {
                "email": "test@test.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "testpassword",
            }
        )

        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password="testpassword",
        )
        payload = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "wrongpassword",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_create_token_no_user(self):
        payload = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "test123",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)

        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_create_token_missing_field(self):
        res = self.client.post(
            TOKEN_URL,
            {"email": "one", "password": ""})
        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class PrivateUserApiTest(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password="testpassword",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_staff": self.user.is_staff,
        },
    )

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})
        self.assertEqual(
            res.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_update_user_profile(self):
        payload = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "test123",
        }

        res = self.client.patch(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        self.assertEqual(self.user.email, payload["email"])
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(self.user.last_name, payload["last_name"])
        self.assertTrue(self.user.check_password(payload["password"]))
