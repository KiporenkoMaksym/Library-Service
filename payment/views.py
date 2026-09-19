from borrowing.tasks import send_telegram_notification_task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import stripe
from django.conf import settings

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentDetailSerializer
)
from user.permissions import IsAuthenticatedOrAdmin

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrAdmin]

    def get_queryset(self):
        queryset = Payment.objects.select_related("borrowing")
        if not self.request.user.is_staff:
            return queryset.filter(borrowing__user=self.request.user)
        return queryset


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.select_related("borrowing")
    serializer_class = PaymentDetailSerializer
    permission_classes = [IsAuthenticatedOrAdmin]

    def get_queryset(self):
        queryset = Payment.objects.all()

        if not self.request.user.is_staff:
            return queryset.filter(borrowing__user=self.request.user)
        return queryset


class PaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response(
                {"error": "No session_id provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == "paid":

            try:
                payment = Payment.objects.select_related(
                    "borrowing__user"
                ).get(session_id=session_id)

                if payment.status != Payment.PaymentStatus.PAID:
                    payment.status = Payment.PaymentType.PAYMENT
                    payment.save(update_fields=["status"])

                    msg = (
                        f"💰 <b>Successful Payment!</b>\n"
                        f"<b>Payment ID:</b> {payment.id}\n"
                        f"<b>Amount:</b> ${payment.money_to_pay}\n"
                        f"<b>User:</b> {payment.borrowing.user.email}"
                    )
                    send_telegram_notification_task.delay(msg)

                return Response(
                    {"message": "Payment was successful!"},
                    status=status.HTTP_200_OK,
                )

            except Payment.DoesNotExist:
                return Response(
                    {"error": "Payment record not found in database."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
                {"message": "Payment not completed yet."},
                status=status.HTTP_400_BAD_REQUEST,
        )


class PaymentCancelView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Payment cancelled. You can pay later within 24 hours."
            },
            status=status.HTTP_200_OK,
        )
