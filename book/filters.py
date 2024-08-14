from django_filters import FilterSet
from django_filters.rest_framework import filters

from book.models import Book


class BookFilter(FilterSet):
    title = filters.CharFilter(
        field_name="title", lookup_expr="icontains"
    )
    author = filters.CharFilter(
        field_name="author", lookup_expr="icontains"
    )

    class Meta:
        model = Book
        fields = ["title", "author"]
