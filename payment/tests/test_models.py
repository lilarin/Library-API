from django.test import TestCase
from django.utils import timezone
from payment.models import Payment
from borrowing.models import Borrowing
from book.models import Book
from user.models import User


class PaymentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )
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

    def test_payment_creation(self):
        self.assertEqual(self.payment.status, Payment.Status.PENDING)
        self.assertEqual(self.payment.payment_type, Payment.Type.PAYMENT)
        self.assertEqual(float(self.payment.money_to_pay), 100.00)
        self.assertEqual(self.payment.session_url, "https://payment-provider.com/session/test")
