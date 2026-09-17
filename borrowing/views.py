from datetime import date

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = (
        Borrowing.objects.all()
        .select_related("user", "book")
    )
    serializer_class = BorrowingSerializer

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        queryset = self.queryset

        if user_id:
            user_ids = self._params_to_ints(user_id)
            queryset = queryset.filter(user_id__in=user_ids)

        if is_active:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def get_serializer_class(self):

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    @action(detail=True, methods=["post"], url_path="return")
    def book_return(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"detail": "Book already returned!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = date.today()
        borrowing.save(update_fields=["actual_return_date"])

        book = borrowing.book
        book.inventory += 1
        book.save(update_fields=["inventory"])

        return Response(
            {"detail": "Book returned successfully"},
            status=status.HTTP_200_OK,
        )
