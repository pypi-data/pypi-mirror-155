import logging

from django.core.management.base import BaseCommand

from openlxp_notifications.management.utils.notification import (
    send_notifications, send_notifications_with_msg)
from openlxp_notifications.models import (EmailConfiguration,
                                          ReceiverEmailConfiguration,
                                          SenderEmailConfiguration)

logger = logging.getLogger('dict_config_logger')


def get_sender_email():
    """Getting sender email id"""

    sender_email_configuration = SenderEmailConfiguration.objects.first()
    if sender_email_configuration:
        sender = sender_email_configuration.sender_email_address
    else:
        sender = None
    return sender


def send_log_email():
    """ function to send emails of log file to personas"""

    # getting email id to send email
    email_data = ReceiverEmailConfiguration.objects.values_list(
        'email_address', flat=True)
    email = list(email_data)
    # Getting sender email id
    sender = get_sender_email()

    if sender and email:
        email_configuration = EmailConfiguration.objects.filter(
            Content_Type='ATTACHMENT').values('HTML_File', 'Subject',
                                              'Email_Content', 'Signature',
                                              'Email_Us', 'FAQ_URL',
                                              'Unsubscribe_Email_ID',
                                              'Content_Type'
                                              ).first()
        if email_configuration:
            send_notifications(email, sender, email_configuration)
        else:
            logger.error("Email configuration for email format not set. "
                         "Email failed to send")
    else:
        logger.error("Sender/Receiver email does not exist. "
                     "Email failed to send")


def send_log_email_with_msg(email, msg):
    """ function to send emails of log file to personas"""
    # Getting sender email id
    sender = get_sender_email()

    if sender:
        email_configuration = EmailConfiguration.objects.filter(
            Content_Type='MESSAGE').values('HTML_File', 'Subject',
                                           'Email_Content', 'Signature',
                                           'Email_Us', 'FAQ_URL',
                                           'Unsubscribe_Email_ID',
                                           'Content_Type'
                                           ).first()
        if email_configuration:
            send_notifications_with_msg(email, sender,
                                        msg, email_configuration)
        else:
            logger.error("Email configuration for email format not set. "
                         "Email failed to send")
    else:
        logger.error("Sender email does not exist. Email failed to send")


class Command(BaseCommand):
    """Django command to send an emails to the filer/personas, when the log
    warning/error occurred in the metadata EVTVL process."""

    def handle(self, *args, **options):
        """Email log notification is sent to filer/personas when warning/error
        occurred in EVTVL process"""
        send_log_email()
