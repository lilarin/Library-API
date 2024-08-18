from book.models import Book
from book.serializers import BookSerializer
from rest_framework import serializers

from borrowing.models import Borrowing
from payment.models import Payment
from user.models import User
from user.serializers import UserSerializer
from payment.serializers import (
    PaymentCreateSerializer,
    PaymentSerializer
)


class UserBorrowingListReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class BookBorrowingListReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "daily_fee"]


class PaymentBorrowingListReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["status", "session_url", "money_to_pay"]


class BorrowingListReadSerializer(serializers.ModelSerializer):
    book = BookBorrowingListReadSerializer()
    user = UserBorrowingListReadSerializer()
    payment = PaymentBorrowingListReadSerializer()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "payment",
            "user",
        ]


class BorrowingRetrieveReadSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = UserSerializer()
    payment = PaymentSerializer()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "payment",
            "user"
        ]


class BorrowingCreateSerializer(serializers.ModelSerializer):

    def validate_book(self, value):
        if value.inventory < 1:
            raise serializers.ValidationError("This book is not available for borrowing.")
        return value

    def validate(self, attrs):
        borrow_date = attrs.get("borrow_date")
        expected_return_date = attrs.get("expected_return_date")

        if expected_return_date and borrow_date and expected_return_date < borrow_date:
            raise serializers.ValidationError(
                {
                    "expected_return_date": (
                        "Expected return date cannot "
                        "be earlier than borrow date."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user

        book = validated_data["book"]
        book.inventory -= 1
        book.save()

        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing

    payment = PaymentCreateSerializer(required=False)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payment"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "actual_return_date": {"read_only": True}
        }


class BorrowingReturnSerializer(serializers.ModelSerializer):
    def validate_actual_return_date(self, value):
        if value is None:
            raise serializers.ValidationError("The return date can't be null.")
        return value

    def validate(self, attrs):
        if self.instance.actual_return_date:
            raise serializers.ValidationError(
                {
                    "non_field_errors": "This borrowing has already returned."
                }
            )
        return attrs

    def update(self, instance, validated_data):
        actual_return_date = validated_data.get("actual_return_date", None)
        instance.actual_return_date = actual_return_date

        if actual_return_date and instance.expected_return_date and actual_return_date > instance.expected_return_date:
            if instance.payment:
                instance.payment.payment_type = Payment.Type.FINE
                instance.payment.status = Payment.Status.PENDING
                instance.payment.save(update_fields=["payment_type", "status"])
            else:
                raise serializers.ValidationError("Payment information is missing.")

        book = instance.book
        book.inventory += 1
        book.save()

        instance.save()
        return instance

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "actual_return_date"
        )
        extra_kwargs = {
            "actual_return_date": {"required": True}
        }
