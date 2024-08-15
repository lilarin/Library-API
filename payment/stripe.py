import stripe


def get_stripe_session(title, amount_to_pay):
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Borrowing: {title}",
                },
                "unit_amount": int(amount_to_pay * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000/api/payment/success?session_id={CHECKOUT_SESSION_ID}/",
        cancel_url="http://127.0.0.1:8000/api/payment/cancel?session_id={CHECKOUT_SESSION_ID/",
    )
