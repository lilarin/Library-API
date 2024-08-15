from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
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
from payment.models import Payment


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
        elif self.action == "return_borrowing":
            return BorrowingReturnSerializer
        return BorrowingCreateSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            raise ValidationError({"detail": str(e)})

    @extend_schema(
        request=BorrowingReturnSerializer,
        responses=BorrowingReturnSerializer,
        description=(
            "Mark borrowing as returned "
            "by setting the actual return date."
        )
    )
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
            partial=False
        )

        serializer.is_valid(raise_exception=True)

        if request.data.get(
                "actual_return_date") and borrowing.expected_return_date:
            actual_return_date = serializer.validated_data.get(
                "actual_return_date")
            if actual_return_date > borrowing.expected_return_date:
                borrowing.payment.payment_type = Payment.Type.FINE

        borrowing.payment.save(update_fields=["payment_type"])
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type={"type": "boolean"},
                description="Filter borrowings by active status (True for active, False for inactive)",
            ),
            OpenApiParameter(
                name="user",
                type={"type": "integer"},
                description="Filter borrowings by user ID",
            ),
        ],
        responses=BorrowingListReadSerializer,
        description="Get list of borrowings with optional filters by active status and user ID."
    )
    def list(self, request, *args, **kwargs):
        """Get list of borrowings."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=BorrowingCreateSerializer,
        responses=BorrowingCreateSerializer,
        description=(
            "Create a new borrowing record. This involves"
            " selecting a book and setting the borrow and "
            "expected return dates. Only authenticated users"
            " can create borrowings."
        )
    )
    def create(self, request, *args, **kwargs):
        """Create a new borrowing."""
        return super().create(request, *args, **kwargs)
