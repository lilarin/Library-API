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
