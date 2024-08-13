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
                url="https://api.telegram.org/bot{0}/{1}".format(
                    token, "sendMessage"
                ),
                data={"chat_id": chat_id, "text": message}
            )
        except requests.exceptions.RequestException as error:
            print(
                f"An error occurred while sending "
                f"message to the TelegramAPI: {error}"
            )
