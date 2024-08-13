import uuid

from django.db import models
from django.utils import timezone

from borrowing.models import Borrowing


class Payment(models.Model):
    """
    The Payment model represents a payment transaction in the library system.
     This model is used to track payments
    made by users for borrowing books or paying fines for late returns.

    Fields:
    - status: Represents the current status of the payment.
      There are two choices:
        - Pending: Indicates that the payment
         has been initiated but not yet completed.

        - Paid: Indicates that the payment has been successfully completed.

    - type: Specifies the type of payment being made.
      There are two choices:
        - Payment: Indicates that the payment is for renting a book.
        - Fine: Indicates that the payment is a fine for
         returning a book after the "Actual return date".

    - borrowing: A ForeignKey linking this
      payment to a specific borrowing record in the system.
      This connects the payment to the corresponding book rental.

    - session_url: The URL where the payment will be processed.
      This is typically a link to the payment page
      provided by the payment processor (Stripe).

    - session_id: A unique identifier for the payment session.
      It is generated when the user initiates the payment process.
      This ID is crucial for tracking
       and managing the payment status through the payment provider.

    - money_to_pay: The total amount that needs to be paid, expressed in USD.
      This amount is calculated based on
      the rental fee for the book or the fine for a late return.
    """

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        max_length=24,
        choices=Status.choices,
        default=Status.PENDING,
    )
    payment_type = models.CharField(
        max_length=24,
        choices=Type.choices,
        default=Type.PAYMENT,
    )
    borrowing = models.OneToOneField(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payment",
    )
    session_url = models.URLField()
    session_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    money_to_pay = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    def __str__(self):
        return f"{self.status} - {self.money_to_pay} - {self.payment_type}"

    class Meta:
        ordering = ["-status"]

    def change_type(self):
        if self.borrowing.actual_return_date:
            if self.borrowing.actual_return_date > self.borrowing.expected_return_date:
                self.payment_type = self.Type.FINE
            else:
                self.payment_type = self.Type.PAYMENT
        else:
            if timezone.now() > self.borrowing.expected_return_date:
                self.payment_type = self.Type.FINE
            else:
                self.payment_type = self.Type.PAYMENT

    @staticmethod
    def validate_positive_money_to_pay(money_to_pay, error_to_raise):
        if money_to_pay < 1:
            raise error_to_raise(
                {
                    "money_to_pay": "money_to_pay cannot be less than 1",
                }
            )

    @staticmethod
    def validate_paid_status(status, session_id, session_url, error_to_raise):
        if status == Payment.Status.PAID:
            if not session_id:
                error_to_raise(
                    {
                        "session_id": "Paid status need a valid session id",
                    }
                )
            if not session_url:
                raise error_to_raise(
                    {
                        "session_url": "session_url cannot be empty",
                    }
                )

    @staticmethod
    def validate_type_payment_status(borrowing, payment_type, error_to_raise):
        if (payment_type == Payment.Type.PAYMENT
                and borrowing.actual_return_date):
            raise error_to_raise(
                {
                    "payment_type": "Cannot pay for returned book",
                }
            )

    @staticmethod
    def validate_borrowing_exists(borrowing, error_to_raise):
        if not borrowing:
            raise error_to_raise(
                {
                    "borrowing": "Payment must be with a borrowing record",
                }
            )

    def clean(self):
        self.validate_positive_money_to_pay(
            self.money_to_pay, ValueError
        )
        self.validate_paid_status(
            self.status, self.session_id, self.session_url, ValueError
        )
        self.validate_type_payment_status(
            self.borrowing, self.payment_type, ValueError
        )
        self.validate_borrowing_exists(
            self.borrowing, ValueError
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
