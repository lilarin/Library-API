from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status", "payment_type", "borrowing",
            "session_url", "session_id", "money_to_pay"
        )


# waiting for borrowing serializers
class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status", "payment_type", "borrowing",
            "session_url", "session_id", "money_to_pay"
        )


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status", "payment_type", "borrowing",
            "session_url", "session_id", "money_to_pay"
        )
