from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from borrowing.models import Borrowing
from book.models import Book
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class BorrowingListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="password"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=1.00,
        )
        self.borrowing_active = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=None,
            book=self.book,
            user=self.user,
        )

        self.borrowing_inactive = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=timezone.now().date(),
            book=self.book,
            user=self.user,
        )
        self.url = reverse("borrowing:borrowing-list")

    def test_list_borrowings_for_authenticated_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_borrowings_admin(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(self.url, {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_borrowings_non_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_is_active_true(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"is_active": "True"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_is_active_false(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"is_active": "False"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_user_id(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url, {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_detail_borrowing_authenticated_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_borrowing_non_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
