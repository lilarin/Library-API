from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    def validate_inventory(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Inventory must be at least 1."
            )
        return value

    def validate_daily_fee(self, value):
        if value < 0.09:
            raise serializers.ValidationError(
                "Daily fee must be at least 0.09."
            )
        return value

    def validate_title(self, value):
        if len(value) < 3 or value.isdigit():
            raise serializers.ValidationError(
                "Send correct title."
            )
        return value

    def validate_author(self, value):
        if value.isdigit() or len(value) < 3 or len(value) > 255:
            raise serializers.ValidationError(
                "Send correct name."
            )
        return value

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee"
        )


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee"
        )
