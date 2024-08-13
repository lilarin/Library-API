from rest_framework import viewsets
from rest_framework.response import Response
from book.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        data = {
            "title": book.title,
            "author": book.author,
            "inventory": book.inventory,
            "daily_fee": book.daily_fee,
        }
        return Response(data)
