from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import permissions, generics
from rest_framework.permissions import IsAuthenticated

from borrowing.filters import BorrowingFilter
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListReadSerializer,
    BorrowingRetrieveReadSerializer,
    BorrowingCreateSerializer
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


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
