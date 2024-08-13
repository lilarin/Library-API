from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentAdminListSerializer,
    # PaymentDetailSerializer
)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.is_staff:
            queryset = Payment.objects.filter(borrowing__user=user)
        else:
            queryset = Payment.objects.all()

        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related(
                "borrowing",
                "borrowing__user",
                "borrowing__book"
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentAdminListSerializer
        # elif self.action == "retrieve":
        #     return PaymentDetailSerializer
        return PaymentSerializer
