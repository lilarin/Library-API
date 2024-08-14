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
            "id", "status", "payment_type", "borrowing",
            "session_url", "session_id", "money_to_pay"
        )


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "money_to_pay",
        )

    def create(self, validated_data):
        with transaction.atomic():
            try:
                payment = Payment.objects.create(**validated_data)
                payment.change_type()
                payment.save()
            except Exception as e:
                raise serializers.ValidationError(
                    {
                        "detail": str(e)
                    }
                )
            return payment

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                    instance.change_type()
                    instance.save()
            except Exception as e:
                raise serializers.ValidationError(
                    {
                        "detail": str(e)
                    }
                )
            return instance

    # def validate(self, attrs):
    #     session_id = attrs.get("session_id")
    #     session_url = attrs.get("session_url")
    #
    #     Payment.validate_positive_money_to_pay(
    #         attrs["money_to_pay"],
    #         serializers.ValidationError
    #     )
    #     Payment.validate_paid_status(
    #         attrs["status"],
    #         session_id,
    #         session_url,
    #         serializers.ValidationError
    #     )
    #     # Payment.validate_type_payment_status(
    #     #     attrs["borrowing"],
    #     #     attrs["payment_type"],
    #     #     serializers.ValidationError
    #     # )
    #     Payment.validate_borrowing_exists(
    #         attrs["borrowing"],
    #         serializers.ValidationError
    #     )
    #     return attrs


#
class PaymentAdminListSerializer(PaymentSerializer):
    borrowing = BorrowingRetrieveReadSerializer(
        read_only=True
    )

    class Meta:
        model = Payment
        fields = (
            "id", "status", "payment_type", "borrowing",
            "session_url", "session_id", "money_to_pay"
        )


class PaymentUserListSerializer(PaymentSerializer):
    borrowing = BorrowingListReadSerializer()


# TODO need to speak about detail page for payment

# waiting for borrowing serializers
# class PaymentDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = (
#             "status", "payment_type", "borrowing",
#             "session_url", "session_id", "money_to_pay"
#         )
