from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse("user:create")
MANAGE_USER_URL = reverse("user:manage_user")


class UserManagerTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@test.com"
        password = "testuser"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        email = "test@test.com"
        password = "testuser"
        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_invalid_user_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, password="testtest")


class PublicUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            "email": "test@test.com",
            "password": "testuser"
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_user_exists(self):
        payload = {
            "email": "test@test.com",
            "password": "testuser"
        }
        get_user_model().objects.create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            "email": "test@test.com",
            "password": "test"
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(email=payload["email"])
        self.assertFalse(user_exist)


class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testuser",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_success(self):
        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": self.user.id,
            "email": self.user.email,
            "is_staff": self.user.is_staff,
        })

    def test_post_me_not_allowed(self):
        response = self.client.post(MANAGE_USER_URL, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {"password": "newpassword123"}

        response = self.client.patch(MANAGE_USER_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
