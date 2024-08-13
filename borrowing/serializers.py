from book.serializers import BookSerializer
from rest_framework import serializers

from borrowing.models import Borrowing
from user.serializers import UserSerializer


class BorrowingListReadSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]


class BorrowingRetrieveReadSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = UserSerializer()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]


class BorrowingCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        book = attrs.get("book")
        borrow_date = attrs.get("borrow_date")
        expected_return_date = attrs.get("expected_return_date")

        if book.inventory < 1:
            raise serializers.ValidationError(
                {"book": "This book is not available for borrowing."}
            )

        if (
            expected_return_date and borrow_date
            and expected_return_date < borrow_date
        ):
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

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        extra_kwargs = {
            "actual_return_date": {"read_only": True},
            "user": {"read_only": True},
        }


class BorrowingReturnSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if self.instance.actual_return_date:
            raise serializers.ValidationError(
                {
                    "non_field_errors": "This borrowing has already returned."
                }
            )
        return attrs

    def update(self, instance, validated_data):
        instance.actual_return_date = validated_data.get(
            "actual_return_date", None
        )

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
