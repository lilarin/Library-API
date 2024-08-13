from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from user.serializers import UserSerializer


class UserSerializerTests(APITestCase):
    def test_create_user(self):
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_update_user_password(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="oldpassword"
        )
        data = {
            "password": "newpassword123"
        }
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password(data["password"]))
