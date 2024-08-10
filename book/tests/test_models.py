from django.test import TestCase
from book.models import Book
from django.core.exceptions import ValidationError


class BookModelTest(TestCase):
    def test_book_creation(self):
        self.book = Book.objects.create(
            title="The Pragmatic Programmer",
            author="Andrew Hunt and David Thomas",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=0.39
        )
        self.assertEqual(str(self.book), '"The Pragmatic Programmer", by Andrew Hunt and David Thomas')
        self.assertEqual(self.book.cover, Book.CoverType.HARD)
        self.assertEqual(self.book.inventory, 5)
        self.assertEqual(self.book.daily_fee, 0.39)

    def test_invalid_cover_choice(self):
        with self.assertRaises(ValidationError):
            book = Book.objects.create(
                title="Invalid Book",
                author="Invalid Author",
                cover="WRONG",
                inventory=1,
                daily_fee=1.00
            )
            book.full_clean()

    def test_inventory_validation(self):
        with self.assertRaises(ValidationError):
            book = Book(
                title="Invalid Inventory",
                author="Author",
                cover=Book.CoverType.HARD,
                inventory=0,
                daily_fee=1.00
            )
            book.full_clean()

    def test_daily_fee_validation(self):
        with self.assertRaises(ValidationError):
            book = Book(
                title="Invalid Fee",
                author="Author",
                cover=Book.CoverType.HARD,
                inventory=1,
                daily_fee=0.05
            )
            book.full_clean()
