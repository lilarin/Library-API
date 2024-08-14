from django.db import transaction
from rest_framework import serializers

from payment.models import Payment
from borrowing.serializers import (
    BorrowingRetrieveReadSerializer,
    BorrowingListReadSerializer
)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "session_url",
            "session_id",
            "money_to_pay"
        )


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "money_to_pay",
        )


class PaymentListSerializer(PaymentSerializer):
    pass
