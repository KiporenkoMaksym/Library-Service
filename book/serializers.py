from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_free",
        )


class BookListSerializer(BookSerializer):
    inventory = serializers.IntegerField(read_only=True)
    daily_free = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_free",
        )


class BookDetailSerializer(BookSerializer):

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_free",
        )
