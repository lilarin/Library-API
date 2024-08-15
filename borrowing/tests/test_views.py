from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from borrowing.models import Borrowing
from book.models import Book
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

User = get_user_model()


class BorrowingReadViewTests(APITestCase):
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
        self.assertEqual(len(response.data), 4)

    def test_list_borrowings_admin(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(self.url, {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_borrowings_non_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_is_active_true(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"is_active": "True"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_filter_is_active_false(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"is_active": "False"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_filter_user_id(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url, {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_detail_borrowing_authenticated_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_borrowing_non_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BorrowingCreateViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Soft",
            inventory=5,
            daily_fee=1.99,
        )
        self.url = reverse("borrowing:borrowing-list")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_create_borrowing_authenticated(self):
        data = {
            "borrow_date": "2024-08-01",
            "expected_return_date": "2024-08-10",
            "book": self.book.id,
        }

        response = self.client.post(self.url, data, format="json")

        self.book.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)
        borrowing = Borrowing.objects.first()
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(self.book.inventory, 4)

    def test_create_borrowing_unauthenticated(self):
        self.client.credentials()
        data = {
            "borrow_date": "2024-08-01",
            "expected_return_date": "2024-08-10",
            "book": self.book.id,
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Borrowing.objects.count(), 0)


class BorrowingReturnTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password123")
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            inventory=10,
            daily_fee=1.50
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date="2024-08-01",
            expected_return_date="2024-08-10",
            book=self.book,
            user=self.user
        )
        self.url = f"/api/borrowing/{self.borrowing.id}/return/"
        self.client.force_authenticate(user=self.user)

    def test_successful_return(self):
        response = self.client.patch(self.url, {"actual_return_date": "2024-08-11"}, format="json")
        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.borrowing.actual_return_date.strftime('%Y-%m-%d'), "2024-08-11")
        self.assertEqual(self.book.inventory, 11)

    def test_return_already_returned_book(self):
        self.borrowing.actual_return_date = "2024-08-11"
        self.borrowing.save()

        response = self.client.patch(self.url, {"actual_return_date": "2024-08-12"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_return_without_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, {"actual_return_date": "2024-08-11"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
