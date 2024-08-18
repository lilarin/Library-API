from celery import shared_task

from borrowing.models import Borrowing
from notification.sender import send_message


@shared_task()
def send_active_borrowings_to_chat():
    active_borrowings = Borrowing.objects.filter(
        actual_return_date__isnull=True
    )
    if active_borrowings:
        message = "Active Borrowings: \n"

        for borrowing in active_borrowings:
            message += f"\n{borrowing}\n"
    else:
        message = "There are no active borrowings."

    send_message(message)


@shared_task
def send_log(message):
    send_message(message)
