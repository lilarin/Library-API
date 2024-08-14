from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)
from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    PaymentListSerializer,
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

    # TODO need to optimize
    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PaymentListSerializer
        elif self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer
