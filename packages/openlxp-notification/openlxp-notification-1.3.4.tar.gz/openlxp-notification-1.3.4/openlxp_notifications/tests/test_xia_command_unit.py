import logging
from unittest.mock import patch

from ddt import ddt
from django.test import tag

from openlxp_notifications.management.commands.conformance_alerts import (
    send_log_email, send_log_email_with_msg)
from openlxp_notifications.models import (EmailConfiguration,
                                          ReceiverEmailConfiguration,
                                          SenderEmailConfiguration)

from .test_setup import TestSetUp

logger = logging.getLogger('dict_config_logger')


@tag('unit')
@ddt
class CommandTests(TestSetUp):

    # Test cases for conformance_alerts

    def test_send_log_email(self):
        """Test for function to send emails of log file to personas with
        attachment"""

        with patch(
                'openlxp_notifications.management.commands.'
                'conformance_alerts.send_notifications',
                return_value=None
        ) as mock_send_notification, \
                patch('openlxp_notifications.models.email_verification',
                      return_value=None):
            receive_email = ReceiverEmailConfiguration(
                email_address=self.receive_email_list1)
            receive_email.save()

            send_email = SenderEmailConfiguration(
                sender_email_address=self.sender_email)
            send_email.save()

            email_config = EmailConfiguration(
                Subject=self.Subject, Email_Content=self.Email_Content,
                Signature=self.Signature, Email_Us=self.Email_Us,
                FAQ_URL=self.FAQ_URL,
                Unsubscribe_Email_ID=self.Unsubscribe_Email_ID,
                Content_Type='ATTACHMENT', HTML_File='HTML_Files/My_Html.html')
            email_config.save()

            send_log_email()
            self.assertEqual(mock_send_notification.call_count, 1)

    def test_send_log_email_with_msg(self):
        """Test for function to send emails of log file to personas with
        message"""
        with patch(
                'openlxp_notifications.management.commands.'
                'conformance_alerts.send_notifications_with_msg',
                return_value=None
        ) as mock_send_notifications_with_msg, \
                patch('openlxp_notifications.models.email_verification',
                      return_value=None):
            send_email = SenderEmailConfiguration(
                sender_email_address=self.sender_email)
            send_email.save()

            email_config = EmailConfiguration(
                Subject=self.Subject, Email_Content=self.Email_Content,
                Signature=self.Signature, Email_Us=self.Email_Us,
                FAQ_URL=self.FAQ_URL,
                Unsubscribe_Email_ID=self.Unsubscribe_Email_ID,
                Content_Type='MESSAGE', HTML_File='HTML_Files/My_Html.html')
            email_config.save()

            send_log_email_with_msg(self.receive_email_list,
                                    'Message')
            self.assertEqual(mock_send_notifications_with_msg.call_count, 1)
