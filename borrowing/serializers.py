from rest_framework import serializers

from borrowing.models import Borrowing, Payment


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


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(
        source="book",
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


class BorrowingDetailSerializer(BorrowingSerializer):
    user = serializers.ReadOnlyField(
        source="first_last_name"
    )
    book = serializers.SlugRelatedField(
        source="book",
        slug_field="title",
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


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = serializers.SlugRelatedField(
        source="borrowing",
        slug_field="first_last_name",
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )

        read_only_fields = (
            "id",
            "status",
            "session_url",
            "session_id",
            "money_to_pay",
        )