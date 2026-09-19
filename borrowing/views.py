from datetime import date

from borrowing.tasks import send_telegram_notification_task
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from payment.models import Payment
from payment.service import create_stripe_session
from .models import Borrowing
from .serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer
)
from user.permissions import IsAuthenticatedOrAdmin

FINE_MULTIPLIER = 2

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = (
        Borrowing.objects.all()
        .select_related("user", "book")
    )
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticatedOrAdmin]

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        user = self.request.user
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if not user.is_staff:
            return queryset.filter(user=user)

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
        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)

        days = (borrowing.expected_return_date - borrowing.borrow_date).days
        if days <= 0:
            days = 1

        money_to_pay = days * borrowing.book.daily_fee

        stripe_session = create_stripe_session(borrowing, money_to_pay)

        Payment.objects.create(
            status=Payment.PaymentStatus.PENDING,
            type=Payment.PaymentType.PAYMENT,
            borrowing=borrowing,
            session_url=stripe_session.url,
            session_id=stripe_session.id,
            money_to_pay=money_to_pay,
        )

        message = (
            f"📖 <b>New Borrowing Created!</b>\n"
            f"<b>Email:</b> {borrowing.user.email}\n"
            f"<b>Book:</b> {borrowing.book.title}\n"
            f"<b>Expected Return Date:</b> {borrowing.expected_return_date}\n"
            f"<b>Payment URL:</b> {stripe_session.url}"
        )

        send_telegram_notification_task.delay(message)

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
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

        payment_url = None
        if borrowing.actual_return_date > borrowing.expected_return_date:
            overdue_days = (
                    borrowing.actual_return_date - borrowing.expected_return_date
            ).days
            fine_amount = overdue_days * book.daily_fee * FINE_MULTIPLIER

            stripe_session = create_stripe_session(borrowing, fine_amount)
            payment_url = stripe_session.url

            Payment.objects.create(
                status=Payment.PaymentStatus.PENDING,
                type=Payment.PaymentType.FINE,
                borrowing=borrowing,
                session_url=stripe_session.url,
                session_id=stripe_session.id,
                money_to_pay=fine_amount,
            )

        msg = (
            f"📚 <b>Book Returned!</b>\n"
            f"<b>User:</b> {borrowing.user.email}\n"
            f"<b>Book:</b> {book.title}\n"
        )
        if payment_url:
            msg += (
                f"⚠️ <b>Overdue fine created:</b> ${fine_amount:.2f}\n"
                f"💳 <a href=\"{payment_url}\">Pay Fine Here</a>"
            )

        send_telegram_notification_task.delay(msg)

        if payment_url:
            return Response(
                {
                    "detail": "Book returned with delay. Please pay the fine.",
                    "fine_payment_url": payment_url,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Book returned successfully"},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Get list of borrowings",
        description="Get a list of borrowings with optional filtering by user_id and is_active.",
        parameters=[
            OpenApiParameter(
                name='user_id',
                type={"type": "array", "items": {"type": "integer"}},
                description="Filter by users id (ex. ?user_id=1,2,3)"
            ),
            OpenApiParameter(
                name='is_active',
                type=bool,
                description="Filter by active borrowing (ex. ?is_active=bool)"
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
