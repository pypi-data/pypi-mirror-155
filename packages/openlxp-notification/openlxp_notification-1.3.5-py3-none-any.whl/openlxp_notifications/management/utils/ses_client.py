import logging

import boto3

logger = logging.getLogger('dict_config_logger')


def email_verification(email):
    """Function to send email verification"""
    logger.info("Check if email id from user is verified")
    # ses = boto3.client('ses')
    # check = check_if_email_verified(email)

    # if check:
    #     logger.error(str(email) + "Email is not verified")
        # logger.info("Email is sent for Verification")
        #
        # response = ses.verify_email_identity(
        #     EmailAddress=email
        # )
        #
        # logger.info(response)


def check_if_email_verified(email):
    """Function to check if email id from user is verified """
    list_emails = list_email_verified()
    if email in list_emails:
        logger.info("Email is already Verified")
        return False
    return True


def list_email_verified():
    """Function to return list of verified emails """

    ses = boto3.client('ses')
    response = ses.list_identities(
        IdentityType='EmailAddress',
        MaxItems=10
    )
    logger.info(response['Identities'])
    return response['Identities']
