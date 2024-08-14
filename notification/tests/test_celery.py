from django.conf import settings
from django.test import TestCase


class CeleryBeatScheduleTest(TestCase):
    def test_task_schedule(self):
        schedule = settings.CELERY_BEAT_SCHEDULE

        task_name = "send-active-borrowings-notification-every-day"
        self.assertIn(task_name, schedule)

        task = schedule[task_name]
        self.assertEqual(task["task"], "notification.tasks.send_active_borrowings_to_chat")
