import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_session(borrowing, amount_usd):
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

        success_url="http://127.0.0.1:8000/payments/success/?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/payments/cancel/",
    )
    return session
