from rest_framework import viewsets
from book.models import Book
from book.serializers import BookSerializer, BookDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BookDetailSerializer
        else:
            return BookSerializer
