from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status", "payment_type", "borrowing",
            "session_url", "session_id", "money_to_pay"
        )

    def validate(self, attrs):
        Payment.validate_positive_money_to_pay(
            attrs["money_to_pay"],
            serializers.ValidationError
        )
        Payment.validate_paid_status(
            attrs["status"],
            attrs["session_id"],
            attrs["session_url"],
            serializers.ValidationError
        )
        Payment.validate_type_payment_status(
            attrs["borrowing"],
            attrs["payment_type"],
            serializers.ValidationError
        )
        Payment.validate_borrowing_exists(
            attrs["borrowing"],
            serializers.ValidationError
        )
        return attrs


# waiting for borrowing serializers
class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status", "payment_type", "borrowing",
            "session_url", "session_id", "money_to_pay"
        )


# waiting for borrowing serializers
class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status", "payment_type", "borrowing",
            "session_url", "session_id", "money_to_pay"
        )
