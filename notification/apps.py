from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = "notification"

    def ready(self):
        from .signals import register_signals
        register_signals()
