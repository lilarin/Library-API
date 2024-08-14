import uuid
from django.db import models


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
        default=Type.PAYMENT
    )
    session_url = models.URLField(
        null=True,
        blank=True
    )
    session_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    money_to_pay = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    def __str__(self):
        return (
            f"Status: {self.status}"
            f"Type: {self.payment_type}"
            f"Status: {self.status}"
            f"Money to pay - {self.money_to_pay}"
        )

    class Meta:
        ordering = ["-status"]

    def save(self, *args, **kwargs):
        base_url = "https://payment-provider.com/session/"
        self.session_url = f"{base_url}{self.session_id}"
        super().save(*args, **kwargs)
