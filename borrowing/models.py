from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from book.models import Book
from library_service import settings
from payment.models import Payment


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
        borrow_days = (self.expected_return_date - self.borrow_date).days

        if borrow_days < 0:
            borrow_days = 0

        base_payment = Decimal(borrow_days) * self.book.daily_fee

        if self.actual_return_date:
            return_days = (self.actual_return_date - self.expected_return_date
                           ).days

            if self.actual_return_date < self.expected_return_date:
                return max(
                    Decimal(0),
                    base_payment - Decimal(
                        abs(return_days)) * self.book.daily_fee
                )
            elif self.actual_return_date > self.expected_return_date:
                # TODO: Can add fine for delay
                return base_payment + Decimal(return_days
                                              ) * self.book.daily_fee

        return base_payment

    def save(self, *args, **kwargs):
        payment = Payment.objects.create(
            money_to_pay=self.calculate_money_to_pay(),
            payment_type=Payment.Type.PAYMENT
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
