from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


class UserViewsTests(APITestCase):
    def test_create_user(self):
        url = reverse("user:create")
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], data["email"])
        self.assertNotIn("password", response.data)

    def test_manage_user(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=user)
        url = reverse("user:manage_user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], user.email)

    def test_manage_user_update(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=user)
        url = reverse("user:manage_user")
        data = {
            "email": "newemail@example.com",
            "password": "newpassword123"
        }
        response = self.client.put(url, data)
        user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
