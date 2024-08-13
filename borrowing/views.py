from rest_framework import viewsets
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)
from rest_framework.permissions import IsAuthenticated

from borrowing.filters import BorrowingFilter
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListReadSerializer,
    BorrowingRetrieveReadSerializer,
    BorrowingCreateSerializer
)


class BorrowingViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
):
    permission_classes = [IsAuthenticated]
    filterset_class = BorrowingFilter
    queryset = Borrowing.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.select_related("book", "user")
        return (Borrowing.objects.filter(user=user)
                .select_related("book", "user"))

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListReadSerializer
        elif self.action == "retrieve":
            return BorrowingRetrieveReadSerializer
        return BorrowingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
