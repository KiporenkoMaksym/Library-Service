import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_session(request, borrowing, amount_usd):
    success_url = request.build_absolute_uri(
        reverse("payments:success")
    ) + "?session_id={CHECKOUT_SESSION_ID}"

    cancel_url = request.build_absolute_uri(
        reverse("payments:cancel")
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Book borrowing: {borrowing.book.title}",
                },
                "unit_amount": int(amount_usd * 100),
            },
            "quantity": 1,
        }],
        mode="payment",

        success_url = success_url,
        cancel_url = cancel_url,
    )
    return session
