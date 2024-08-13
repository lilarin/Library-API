from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from book.models import Book
from borrowing.models import Borrowing

User = get_user_model()


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
        self.url = reverse("borrowing:borrowing-create")

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
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data}")

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
