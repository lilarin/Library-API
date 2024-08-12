from rest_framework import serializers
from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        inventory = attrs.get("inventory")
        daily_fee = attrs.get("daily_fee")
        title = attrs.get("title")

        if inventory is not None and inventory < 1:
            raise serializers.ValidationError({"inventory": "Inventory must be at least 1."})

        if daily_fee is not None and daily_fee < 0.09:
            raise serializers.ValidationError({"daily_fee": "Daily fee must be at least 0.09."})

        if title is None:
            raise serializers.ValidationError({"title": "Title cannot be empty."})

        return attrs

    class Meta:
        model = Book
        fields = ("title", "author", "cover", "inventory", "daily_fee")
