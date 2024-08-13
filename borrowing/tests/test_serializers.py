from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from borrowing.models import Borrowing
from book.models import Book
from borrowing.serializers import (
    BorrowingListReadSerializer,
    BorrowingRetrieveReadSerializer,
)
from user.models import User


class BorrowingSerializersTests(APITestCase):
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

        self.borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=None,
            book=self.book,
            user=self.user,
        )

    def test_borrowing_list_read_serializer(self):
        serializer = BorrowingListReadSerializer(instance=self.borrowing)
        data = serializer.data

        self.assertEqual(
            set(data.keys()),
            {
                "id",
                "borrow_date",
                "expected_return_date",
                "actual_return_date",
                "book",
                "user",
            },
        )
        self.assertEqual(data["book"]["title"], self.book.title)
        self.assertEqual(data["user"], self.user.id)

    def test_borrowing_retrieve_read_serializer(self):
        serializer = BorrowingRetrieveReadSerializer(instance=self.borrowing)
        data = serializer.data

        self.assertEqual(
            set(data.keys()),
            {
                "id",
                "borrow_date",
                "expected_return_date",
                "actual_return_date",
                "book",
                "user",
            },
        )
        self.assertEqual(data["book"]["title"], self.book.title)
        self.assertEqual(data["user"]["email"], self.user.email)
