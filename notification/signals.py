from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.sender import send_message
from borrowing.models import Borrowing


@receiver(post_save, sender=Borrowing)
def after_saving_borrowing(sender, instance, created, **kwargs):
    if created:
        message = f"New Borrowing: \n{instance}"
        send_message(message)
