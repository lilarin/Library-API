from rest_framework import viewsets
from rest_framework.response import Response

from book.models import Book
from rest_framework.decorators import action
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['get'], url_path='detail')
    def detail(self, request, pk=None):
        book = self.get_object()
        data = {
            "title": book.title,
            "author": book.author,
            "inventory": book.inventory,
            "daily_fee": book.daily_fee,
            "some_additional_stat": "Example statistic"
        }
        return Response(data)
