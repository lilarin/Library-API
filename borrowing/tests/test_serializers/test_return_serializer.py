from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from borrowing.models import Borrowing
from book.models import Book
from borrowing.serializers import BorrowingReturnSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class BorrowingReturnSerializerTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password123")
        self.book = Book.objects.create(title="Test Book", author="Author", inventory=10, daily_fee=1.50)
        self.borrowing = Borrowing.objects.create(
            borrow_date="2024-08-01",
            expected_return_date="2024-08-10",
            book=self.book,
            user=self.user
        )

    def test_successful_return(self):
        data = {"actual_return_date": "2024-08-11"}
        serializer = BorrowingReturnSerializer(instance=self.borrowing, data=data)

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(self.borrowing.actual_return_date.strftime("%Y-%m-%d"), "2024-08-11")
        self.assertEqual(self.book.inventory, 11)

    def test_already_returned_book(self):
        self.borrowing.actual_return_date = "2024-08-11"
        self.borrowing.save()

        data = {"actual_return_date": "2024-08-12"}
        serializer = BorrowingReturnSerializer(instance=self.borrowing, data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_missing_actual_return_date(self):
        data = {}
        serializer = BorrowingReturnSerializer(instance=self.borrowing, data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("actual_return_date", serializer.errors)
