from django.db import transaction
from rest_framework import serializers

from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
        )
        read_only_fields = ("id", "actual_return_date", "user")

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]

            if book.inventory <= 0:
                raise serializers.ValidationError("Book is out of stock")

            borrowing = Borrowing.objects.create(**validated_data)

            book.inventory -= 1
            book.save(update_fields=["inventory"])
            return borrowing


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
        extra_kwargs = {"actual_return_date": {"required": True}, "read_only": False}


class BorrowingDetailSerializer(BorrowingSerializer):
    user = serializers.ReadOnlyField(
        source="user.email"
    )
    book = serializers.SlugRelatedField(
        slug_field="title",
        read_only=True,
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
        )
