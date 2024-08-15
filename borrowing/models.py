from decimal import Decimal

import stripe
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from book.models import Book
from library_service import settings
from payment.models import Payment
from payment.stripe import get_stripe_session


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
    )

    def clean(self):
        if self.expected_return_date < self.borrow_date:
            raise ValidationError(_(
                "Expected return date cannot be earlier than borrow date."
            ))
        if self.actual_return_date:
            if self.actual_return_date < self.borrow_date:
                raise ValidationError(_(
                    "Actual return date cannot be earlier than borrow date."
                ))

    def calculate_money_to_pay(self):
        if isinstance(self.expected_return_date, str):
            self.expected_return_date = timezone.datetime.strptime(
                self.expected_return_date, "%Y-%m-%d"
            ).date()

        if isinstance(self.borrow_date, str):
            self.borrow_date = timezone.datetime.strptime(
                self.borrow_date, "%Y-%m-%d"
            ).date()

        borrow_days = (self.expected_return_date - self.borrow_date).days

        if borrow_days < 0:
            borrow_days = 0

        daily_fee_decimal = Decimal(str(self.book.daily_fee))
        base_payment = Decimal(borrow_days) * daily_fee_decimal

        if self.actual_return_date:
            if isinstance(self.actual_return_date, str):
                self.actual_return_date = timezone.datetime.strptime(
                    self.actual_return_date, "%Y-%m-%d"
                ).date()

            return_days = (
                self.actual_return_date - self.expected_return_date
            ).days
            if return_days < 1:
                return_days += 1

            if self.actual_return_date < self.expected_return_date:
                return max(
                    Decimal(0),
                    base_payment - Decimal(
                        abs(return_days)
                    ) * daily_fee_decimal
                )
            elif self.actual_return_date > self.expected_return_date:
                # TODO: Can add fine for delay
                return base_payment + Decimal(
                    return_days
                ) * daily_fee_decimal

        return base_payment

    def money_for_fine(self):
        ...

    def save(self, *args, **kwargs):
        amount_to_pay = self.calculate_money_to_pay()

        stripe.api_key = settings.STRIPE_SECRET_KEY

        session = get_stripe_session(self.book.title, amount_to_pay)

        payment = Payment.objects.create(
            money_to_pay=amount_to_pay,
            payment_type=Payment.Type.PAYMENT,
            session_id=session.id,
            session_url=session.url,
        )
        self.payment = payment

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        data = (
            f"Book: {self.book}\n"
            f"Borrowed by: {self.user.email}\n"
            f"Borrow date: {self.borrow_date}\n"
            f"Expected return date: {self.expected_return_date}"
        )
        if self.actual_return_date:
            data += f"\nActual return date: {self.actual_return_date}"
        return data

    class Meta:
        ordering = ["expected_return_date"]
