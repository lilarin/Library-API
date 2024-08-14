from django.test import TestCase
from payment.models import Payment
from payment.serializers import PaymentSerializer
from borrowing.models import Borrowing
from book.models import Book
from user.models import User
from django.utils import timezone


class PaymentSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@test.com", password="test1password")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="SOFT",
            inventory=5,
            daily_fee="1.00"
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timezone.timedelta(days=1),
            book=self.book,
            user=self.user
        )
        self.payment = Payment.objects.create(
            status=Payment.Status.PENDING,
            payment_type=Payment.Type.PAYMENT,
            borrowing=self.borrowing,
            session_url="https://payment-provider.com/session/test",
            money_to_pay="100.00"
        )

    def test_payment_serializer_valid(self):
        serializer = PaymentSerializer(instance=self.payment)
        data = serializer.data
        self.assertEqual(data["status"], Payment.Status.PENDING)
        self.assertEqual(data["payment_type"], Payment.Type.PAYMENT)
        self.assertEqual(data["money_to_pay"], "100.00")
        self.assertEqual(data["session_url"], "https://payment-provider.com/session/test")

    def test_payment_serializer_create(self):
        new_borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timezone.timedelta(days=2),
            book=self.book,
            user=self.user
        )
        data = {
            "status": Payment.Status.PENDING,
            "payment_type": Payment.Type.PAYMENT,
            "borrowing": new_borrowing.id,
            "session_url": "https://payment-provider.com/session/test",
            "money_to_pay": "150.00"
        }
        serializer = PaymentSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)

        self.assertTrue(serializer.is_valid())
        payment = serializer.save()
        self.assertEqual(float(payment.money_to_pay), 150.00)
        self.assertEqual(payment.status, Payment.Status.PENDING)

    def test_payment_serializer_update(self):
        new_borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timezone.timedelta(days=2),
            book=self.book,
            user=self.user
        )
        data = {
            "status": Payment.Status.PAID,
            "borrowing": new_borrowing.id,
            "money_to_pay": "200.00",
            "session_url": "https://payment-provider.com/session/test"
        }
        serializer = PaymentSerializer(instance=self.payment, data=data, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)

        self.assertTrue(serializer.is_valid())
        payment = serializer.save()
        self.assertEqual(float(payment.money_to_pay), 200.00)
        self.assertEqual(payment.status, Payment.Status.PAID)
