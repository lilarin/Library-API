from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from borrowing.models import Borrowing
from book.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=5,
            daily_fee=1.99,
        )

    def test_borrowing_is_valid(self):
        borrowing = Borrowing(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=None,
            book=self.book,
            user=self.user,
        )
        try:
            borrowing.full_clean()
        except ValidationError as e:
            self.fail(f"Borrowing instance raised ValidationError: {e}")

    def test_expected_return_date_before_borrow_date_raise_error(self):
        borrowing = Borrowing(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() - timedelta(days=1),
            actual_return_date=None,
            book=self.book,
            user=self.user,
        )
        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_actual_return_date_before_borrow_date_raise_error(self):
        borrowing = Borrowing(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=timezone.now().date() - timedelta(days=1),
            book=self.book,
            user=self.user,
        )
        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_correct_str_method(self):
        borrowing = Borrowing(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=None,
            book=self.book,
            user=self.user,
        )
        expected_str = (
            f"Book: {self.book}\n"
            f"Borrowed by: {self.user.email}\n"
            f"Borrow date: {borrowing.borrow_date}\n"
            f"Expected return date: {borrowing.expected_return_date}"
        )
        self.assertEqual(str(borrowing), expected_str)
