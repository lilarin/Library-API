from django.test import TestCase
from book.models import Book
from book.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="The Pragmatic Programmer",
            author="Andrew Hunt and David Thomas",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=0.39
        )

    def test_valid_serializer(self):

        serializer = BookSerializer(instance=self.book)

        data = serializer.data

        self.assertEqual(data["title"], self.book.title)
        self.assertEqual(data["author"], self.book.author)
        self.assertEqual(data["cover"], self.book.cover)
        self.assertEqual(data["inventory"], self.book.inventory)
        self.assertEqual(data["daily_fee"], str(self.book.daily_fee))
