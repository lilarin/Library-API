from django.test import TestCase
from payment.models import Payment


class PaymentModelTests(TestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            status=Payment.Status.PENDING,
            payment_type=Payment.Type.PAYMENT,
            session_url="https://payment-provider.com/session/test",
            money_to_pay="100.00"
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.status, Payment.Status.PENDING)
        self.assertEqual(self.payment.payment_type, Payment.Type.PAYMENT)
        self.assertEqual(float(self.payment.money_to_pay), 100.00)
        self.assertEqual(self.payment.session_url, "https://payment-provider.com/session/test")
