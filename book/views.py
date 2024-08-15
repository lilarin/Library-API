from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter
)
from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

from book.filters import BookFilter
from book.models import Book
from book.permissions import IsAdminOrReadOnly
from book.serializers import (
    BookSerializer,
    BookDetailSerializer
)


class BookViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    queryset = Book.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type={"type": "string"},
                description="Filter books by title"
            ),
            OpenApiParameter(
                name="author",
                type={"type": "string"},
                description="Filter books by author"
            ),
        ],
        responses=BookSerializer,
        description=(
            "Get list of books with optional filters by title,"
            " author, cover type, inventory, or daily fee."
        )
    )
    def list(self, request, *args, **kwargs):
        """Get list of books."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=BookSerializer,
        responses=BookSerializer,
        description="Create a new book. Only admin users can create books."
    )
    def create(self, request, *args, **kwargs):
        """Create a new book."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=BookSerializer,
        responses=BookSerializer,
        description=(
            "Update an existing book. "
            "Only admin users can update books."
        )
    )
    def update(self, request, *args, **kwargs):
        """Update a book."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses=None,
        description="Delete a book. Only admin users can delete books."
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a book."""
        return super().destroy(request, *args, **kwargs)
