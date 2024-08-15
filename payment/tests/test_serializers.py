from django.test import TestCase
from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentSerializerTests(TestCase):

    def setUp(self):
        self.payment = Payment.objects.create(
            status=Payment.Status.PENDING,
            payment_type=Payment.Type.PAYMENT,
            session_url="https://payment-provider.com/session/test",
            money_to_pay="100.00"
        )

    def test_payment_serializer_valid(self):
        serializer = PaymentSerializer(instance=self.payment)
        data = serializer.data
        self.assertEqual(data["status"], Payment.Status.PENDING)
        self.assertEqual(data["money_to_pay"], "100.00")
        self.assertEqual(data["session_url"], "https://payment-provider.com/session/test")

    def test_payment_serializer_create(self):
        data = {
            "status": Payment.Status.PENDING,
            "payment_type": Payment.Type.PAYMENT,
            "session_url": "https://payment-provider.com/session/test",
            "session_id": "asdadasdadad",
            "money_to_pay": "150.00"
        }
        serializer = PaymentSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        payment = serializer.save()
        self.assertEqual(float(payment.money_to_pay), 150.00)
        self.assertEqual(payment.status, Payment.Status.PENDING)

    def test_payment_serializer_update(self):
        data = {
            "status": Payment.Status.PAID,
            "money_to_pay": "200.00",
            "session_url": "https://payment-provider.com/session/test"
        }
        serializer = PaymentSerializer(instance=self.payment, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        payment = serializer.save()
        self.assertEqual(float(payment.money_to_pay), 200.00)
        self.assertEqual(payment.status, Payment.Status.PAID)
