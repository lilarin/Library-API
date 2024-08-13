from rest_framework import serializers
from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        book = attrs.get("book")
        expected_return_date = attrs.get("expected_return_date")
        borrow_date = attrs.get("borrow_date")
        actual_return_date = attrs.get("actual_return_date")

        if book.inventory < 1:
            raise serializers.ValidationError(
                {"book": "This book is not available for borrowing."}
            )

        if expected_return_date < borrow_date:
            raise serializers.ValidationError(
                {"expected_return_date": "Expected return date cannot be earlier than borrow date."}
            )

        if actual_return_date and actual_return_date < borrow_date:
            raise serializers.ValidationError(
                {"actual_return_date": "Actual return date cannot be earlier than borrow date."}
            )

        return attrs

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
