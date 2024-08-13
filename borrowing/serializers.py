from rest_framework import serializers
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
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
                    "expected_return_date": "Expected return date "
                    "cannot be earlier than borrow date."
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
            "user": {"read_only": True}
        }
