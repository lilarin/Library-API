from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import permissions, generics

from borrowing.filters import BorrowingFilter
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListReadSerializer,
    BorrowingRetrieveReadSerializer,
)


class BaseBorrowingView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.select_related("book", "user")
        return (Borrowing.objects.filter(user=user)
                .select_related("book", "user"))


class BorrowingListView(BaseBorrowingView, generics.ListAPIView):
    serializer_class = BorrowingListReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowingFilter


class BorrowingDetailView(BaseBorrowingView, generics.RetrieveAPIView):
    serializer_class = BorrowingRetrieveReadSerializer
