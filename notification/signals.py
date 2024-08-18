from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.tasks import send_log
from borrowing.models import Borrowing
from payment.models import Payment


@receiver(post_save, sender=Borrowing)
def after_saving_borrowing(sender, instance, created, **kwargs):
    if created:
        message = f"New Borrowing: \n{instance}"
        send_log.delay(message)


@receiver(post_save, sender=Payment)
def after_changing_payment(sender, instance, created, **kwargs):
    if not created:
        message = f"New Payment: \n{instance}"
        send_log.delay(message)
