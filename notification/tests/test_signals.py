from django.test import TestCase
from unittest.mock import patch
from notification.tasks import send_active_borrowings_to_chat


class SendActiveBorrowingsToChatTest(TestCase):
    @patch("notification.tasks.send_message")
    @patch("borrowing.models.Borrowing.objects.filter")
    def test_send_active_borrowings_exception(self, mock_filter, mock_send_message):
        mock_filter.side_effect = Exception("Database error")

        with self.assertRaises(Exception):
            send_active_borrowings_to_chat.delay()

        mock_send_message.assert_not_called()
