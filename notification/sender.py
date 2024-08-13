import os
from dotenv import load_dotenv
import requests

load_dotenv()
token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_NOTIFICATION_CHANNEL")


def send_message(message):
    if token and chat_id:
        try:
            requests.post(
                url=f"https://api.telegram.org/bot{token}/sendMessage",  # noqa: E231
                data={
                    "chat_id": chat_id,
                    "text": message
                }
            )
        except requests.exceptions.RequestException as error:
            print(
                "An error occurred while sending "
                f"message to the Telegram API: {error}"
            )
