import logging

import socket
from time import sleep
from io import BytesIO

from django.core import mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage

from django.conf import settings

from django.contrib.auth.models import User, Group

from core.setup_logic import Credentials

log = logging.getLogger("core")
log_mail = logging.getLogger("mail")

curr_hostname = getattr(settings, 'CURR_HOSTNAME', None)

CONNECTION = None


def connection_ok():
    if CONNECTION is None:
        return False
    elif CONNECTION is not None:
        try:
            if CONNECTION.open():
                return True
        except socket.gaierror:
            return False
    else:
        return True


# https://docs.djangoproject.com/en/4.1/topics/email/#sending-multiple-emails
def make_connection(retry_i=3, wait_s=10):
    """
    Open connection or use one opened already.
    """
    global CONNECTION
    # None is never opened, False is if it is closed - reopened and save:
    if not connection_ok():
        try:
            CONNECTION = mail.get_connection()
        # RECURSION!
        except socket.gaierror as e:
            CONNECTION = None
            while retry_i > 1:
                log.info(f"Try {retry_i}: on exception - open email connection")
                sleep(wait_s)
                retry_i -= 1
                make_connection(retry_i, wait_s)
                if retry_i < 1:
                    msg = f"Cannot send an email, connection is not open or cannot be open. Exception: {e}"
                    log.error(msg)
                    log_mail.error(msg)
                    raise Exception(msg)
            else:
                log.error(f"Connection retries ended ({retry_i}), exit!")
        finally:
            log.debug(f'Connection established: {CONNECTION}')
    else:
        log.debug(f"Email connection is open, use saved CONNECTION")


def email_retry(email, retry_i=3, wait_s=10):
    """
    Retry email sends if it fails.
    """
    try:
        email.send()
    # If socket error - try to reopen connection, 3 times:
    except socket.gaierror:
        make_connection(3, 10)
    # Now catch generic exception, but collect errors and add exceptions.
    except Exception as e:
        while retry_i > 1:
            log.error(f"Try: {retry_i}: retry - send email")
            sleep(wait_s)
            retry_i -= 1
            email_retry(email, retry_i, wait_s)
            if retry_i > 1:
                msg = f"Cannot send an email, error during mail.send(). Exception: {e}"
                log.error(msg)
                log_mail.error(msg)
                raise Exception(msg)
        else:
            log.error(f"Re-send retried ended ({retry_i}), exit!")
    finally:
        log.debug(f'Finish mail sending loop!')


class Mails:

    def __init__(self):
        make_connection(5, 10)

    def get_group_or_user_recipients(self, recipients_list=None):
        """
        Use a list of sting args and check if each is a mailing group or user.
        Make a list of emails and return.
        Never use plain emails, only users from database or groups.
        :return: list
        """
        if recipients_list is None:
            return []
        if isinstance(recipients_list, str):
            log.info(f"Recipients list is a string, trying to split by ',' as default. ")
            recipients_list = recipients_list.split(',')
        return self.check_users_and_groups(recipients_list)

    @staticmethod
    def check_users_and_groups(names_list):
        """
        Iter over all groups and all users in Django DB to collect related emails for each user.
        Check duplicates.

        :param names_list:
        :return:
        """
        validated_emails_list = []
        for name_str in names_list:
            # Possibly can be an empty string after a split list of strings.
            if name_str and isinstance(name_str, str) and '@' not in name_str:
                # Check if there is a group with name:
                if Group.objects.filter(name__exact=name_str).exists():
                    group = Group.objects.get(name__exact=name_str)
                    for user in group.user_set.all():
                        if user.email not in validated_emails_list:
                            validated_emails_list.append(user.email)
                # In case if all groups checked - check user at last
                elif User.objects.filter(username__exact=name_str).exists():
                    user_email = User.objects.get(username__exact=name_str).email
                    if user_email not in validated_emails_list:
                        validated_emails_list.append(user_email)
                else:
                    log.error(f"This string was not found as User nor Group! -'{name_str}'- ")
            elif isinstance(name_str, str) and '@' in name_str:
                log.info(f"Be aware, this is a raw email in list, with @ in a string. {name_str}")
                validated_emails_list.append(name_str)
            # In some cases, there could be an empty list as recipient, so we'll skip it, even that it is not an issue.
            else:
                log.info(f"This is not a string or not having any @ in it, skipping validation: {name_str}")
        return validated_emails_list

    def short(self, **mail_args):
        """
        Get the args to fill mail with to, cc, subject and text and send.
        https://docs.djangoproject.com/en/2.0/topics/email/

        :param mail_args: dict
        :return:
        """
        attachments = mail_args.get('attachments', {})
        mail_html = mail_args.get('mail_html', '')
        body = mail_args.get('body', False)
        subject = mail_args.get('subject', False)

        send_to = mail_args.get('send_to', 'email.service.error')  # Send to me, if None.
        send_cc = mail_args.get('send_cc', None)
        bcc = mail_args.get('bcc', None)

        send_to = self.get_group_or_user_recipients(send_to)
        send_cc = self.get_group_or_user_recipients(send_cc)
        bcc = self.get_group_or_user_recipients(bcc)

        images = mail_args.get('images', [])
        attach_file = mail_args.get('attach_file', '')
        attach_content = mail_args.get('attach_content', '')
        attach_content_name = mail_args.get('attach_content_name', 'octopus.html')

        assert isinstance(send_to, list), 'send_to should be a list!'
        assert isinstance(send_cc, list), 'send_cc should be a list!'
        assert isinstance(bcc, list), 'bcc should be a list!'

        txt = '{} {} host: {}'
        if not body and not mail_html:
            body = txt.format('No txt body added.', '\n', Credentials.HOSTNAME)
        else:
            body = "{} \n\t\tOn host: {}".format(body, Credentials.HOSTNAME)

        if not subject:
            subject = txt.format('No Subject added', ' - ', Credentials.HOSTNAME)

        email_args = dict(
            subject=subject,
            body=body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            to=send_to,
            cc=send_cc,
            bcc=bcc,
            connection=CONNECTION,
        )

        # When email is an HTML composed file:
        if mail_html:
            email = EmailMultiAlternatives(**email_args)
            email.attach_alternative(mail_html, "text/html")
        else:
            # Plain test email with possible attachments as text
            email = EmailMessage(**email_args)

        # When multiple or ONE attachment:
        if attachments:
            for attach_content_name, attach_content in attachments.items():
                email.attach(filename=attach_content_name, content=attach_content, mimetype="text/html")
        else:
            if attach_file:
                email.attach_file(attach_file)
            if attach_content:
                email.attach(attach_content_name, attach_content, "text/html")

        # Image embedded in body and attached to mail
        # Only send images with HTML bodied emails!
        if images and mail_html:
            iter_img = 0
            for image in images:
                iter_img += 1
                stream = BytesIO()
                image.save(stream, format="PNG", quality=100)
                stream.seek(0)
                imgObj = stream.read()
                img = MIMEImage(imgObj)
                img.add_header('Content-ID', '<image>')
                email.attach(img)

        email_retry(email, 3, 10)
        return True
