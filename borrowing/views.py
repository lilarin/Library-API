from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.filters import BorrowingFilter
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListReadSerializer,
    BorrowingRetrieveReadSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer
)


class BorrowingViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
):
    filterset_class = BorrowingFilter
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.select_related("book", "user")
        return Borrowing.objects.filter(
            user=user
        ).select_related("book", "user")

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListReadSerializer
        elif self.action == "retrieve":
            return BorrowingRetrieveReadSerializer
        return BorrowingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["patch"],
        url_path="return",
        permission_classes=[IsAuthenticated]
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        serializer = BorrowingReturnSerializer(
            borrowing,
            data=request.data,
            context={"request": request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
