from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)
from payment.models import Payment
from payment.serializers import (
    PaymentSerializer, PaymentListSerializer, PaymentCreateSerializer,
)


class PaymentViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        elif self.action == "create":
            return PaymentCreateSerializer
        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="status",
                type={"type": "string"},
                enum=["PENDING", "PAID"],
                description="Filter payments by status (PENDING or PAID)"
            ),
            OpenApiParameter(
                name="payment_type",
                type={"type": "string"},
                enum=["PAYMENT", "FINE"],
                description="Filter payments by type (PAYMENT or FINE)"
            ),
            OpenApiParameter(
                name="money_to_pay",
                type={"type": "number", "format": "float"},
                description="Filter payments by amount to pay"
            ),
        ],
        responses=PaymentListSerializer,
        description=(
            "Get list of payments with optional filters"
            " by status, payment type, or amount to pay."
        )
    )
    def list(self, request, *args, **kwargs):
        """Get list of payments."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=PaymentSerializer,
        description="Retrieve details of a specific payment by its ID."
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a payment."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=PaymentCreateSerializer,
        responses=PaymentCreateSerializer,
        description=(
            "Create a new payment record."
            " Only authenticated users can create payments."
        )
    )
    def create(self, request, *args, **kwargs):
        """Create a new payment."""
        return super().create(request, *args, **kwargs)
