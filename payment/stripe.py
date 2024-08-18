from django.conf import settings

import stripe
from rest_framework.response import Response
from stripe import StripeError

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(title, amount):
    try:
        payment_url = "http://127.0.0.1:8000/api/payment/"
        session_id = "?session_id={CHECKOUT_SESSION_ID}"
        return stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Borrowing: {title}",
                    },
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{payment_url}success/{session_id}",
            cancel_url=f"{payment_url}cancel/{session_id}",
        )
    except StripeError as error:
        return Response(
            {"error": f"Failed to create Stripe session: {error}"},
            status=400
        )


def get_stripe_session(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except StripeError as error:
        return Response(
            {"error": f"Failed to retrieve Stripe session: {error}"},
            status=400
        )
