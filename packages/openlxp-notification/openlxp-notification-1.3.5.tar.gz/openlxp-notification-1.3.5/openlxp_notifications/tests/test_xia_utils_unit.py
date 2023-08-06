import logging
from unittest.mock import mock_open, patch

from ddt import ddt
from django.test import tag

from openlxp_notifications.management.utils.notification import (
    send_notifications, send_notifications_with_msg)
from openlxp_notifications.management.utils.ses_client import \
    check_if_email_verified
from openlxp_notifications.models import EmailConfiguration

from .test_setup import TestSetUp

logger = logging.getLogger('dict_config_logger')


@tag('unit')
@ddt
class UtilsTests(TestSetUp):
    """Unit Test cases for utils """

    # Test cases for NOTIFICATION
    def test_check_if_email_verified(self):
        """Test to check if email id from user is verified """
        with patch('openlxp_notifications.management.utils.ses_client'
                   '.list_email_verified') as mock_list:
            mock_list.return_value = self.receive_email_list
            email_value = 'receiver1@openlxp.com'
            return_val = check_if_email_verified(email_value)
            self.assertFalse(return_val)

    def test_check_if_email_not_verified(self):
        """Test to check if email id from user is verified """
        with patch('openlxp_notifications.management.utils.ses_client'
                   '.list_email_verified') as mock_list:
            mock_list.return_value = self.receive_email_list
            email_value = 'receiver2@openlxp.com'
            return_val = check_if_email_verified(email_value)
            self.assertTrue(return_val)

    def test_send_notifications(self):
        """Test for the function  which sends email of a log file """
        with patch('openlxp_notifications.management.utils.notification'
                   '.EmailMessage') as mock_send, \
                patch('openlxp_notifications.management.utils.ses_client'
                      '.boto3.client'), \
                patch('openlxp_notifications.management.utils.notification'
                      '.send_notifications'), \
                patch(
                    'openlxp_notifications.management.utils.notification.'
                    'open', mock_open(read_data="data")):
            email_config = EmailConfiguration(
                Subject=self.Subject, Email_Content=self.Email_Content,
                Signature=self.Signature, Email_Us=self.Email_Us,
                FAQ_URL=self.FAQ_URL,
                Unsubscribe_Email_ID=self.Unsubscribe_Email_ID,
                Content_Type='ATTACHMENT', HTML_File='HTML_Files/My_Html.html')
            email_config.save()
            email_configuration = EmailConfiguration.objects.filter(
                Content_Type='ATTACHMENT').values('HTML_File', 'Subject',
                                                  'Email_Content',
                                                  'Signature', 'Email_Us',
                                                  'FAQ_URL',
                                                  'Unsubscribe_Email_ID',
                                                  'Content_Type'
                                                  ).first()
            send_notifications(self.receive_email_list, self.sender_email,
                               email_configuration)

            self.assertEqual(mock_send.call_count, 2)

    def test_send_notifications_with_msg(self):
        """Test for the function  which sends email of a message """
        with patch('openlxp_notifications.management.utils.notification'
                   '.EmailMessage') as mock_send, \
                patch('openlxp_notifications.management.utils.ses_client'
                      '.boto3.client'), \
                patch('openlxp_notifications.management.utils.notification'
                      '.send_notifications'), \
                patch(
                    'openlxp_notifications.management.utils.notification.'
                    'open', mock_open(read_data="data")):
            email_config = EmailConfiguration(
                Subject=self.Subject, Email_Content=self.Email_Content,
                Signature=self.Signature, Email_Us=self.Email_Us,
                FAQ_URL=self.FAQ_URL,
                Unsubscribe_Email_ID=self.Unsubscribe_Email_ID,
                Content_Type='MESSAGE', HTML_File='HTML_Files/My_Html.html')
            email_config.save()
            email_configuration = EmailConfiguration.objects.filter(
                Content_Type='MESSAGE').values('HTML_File', 'Subject',
                                               'Email_Content',
                                               'Signature', 'Email_Us',
                                               'FAQ_URL',
                                               'Unsubscribe_Email_ID',
                                               'Content_Type'
                                               ).first()
            send_notifications_with_msg(self.receive_email_list,
                                        self.sender_email, 'Message',
                                        email_configuration)

            self.assertEqual(mock_send.call_count, 2)
