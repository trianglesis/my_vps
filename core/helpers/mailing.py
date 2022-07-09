import logging
from time import sleep
from io import BytesIO

from django.core import mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage

from django.conf import settings

from django.contrib.auth.models import User, Group

log = logging.getLogger("core")
curr_hostname = getattr(settings, 'CURR_HOSTNAME', None)


class Mails:

    def get_group_or_user_recipients(self, recipients_list=None):
        """
        Use list of sting args and check if each is a mailing group or user.
        Make list of emails and return.
        Never use plain emails, only users from database or groups.
        :return: list
        """

        if recipients_list is None:
            return []

        log.debug(f"recipients_list: {recipients_list}")
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
            # Possibly can be an empty string after split list of strings.
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

                # Check user custom_name values too!
                # User name in django usually differ from user custom_name account name.
                # CUSTOM_NAME value is added by SITE Admin into the related column manually when user register first.
                elif User.objects.filter(user_profile__custom_name_username__exact=name_str).exists():
                    user_email = User.objects.filter(user_profile__custom_name_username__exact=name_str).first().email
                    validated_emails_list.append(user_email)

                else:
                    log.error(f"This string was not found as User nor Group! -'{name_str}'- ")
            elif isinstance(name_str, str) and '@' in name_str:
                log.info(f"Be aware, this is a raw email in list, with @ in a string. {name_str}")
                validated_emails_list.append(name_str)
            # In some cases there could be an empty list as recipient, so we'll skip it, even that it is not an issue.
            else:
                log.info(f"This is not a string or not having any @ in it, skipping validation: {name_str}")

        log.debug(f"validated_emails_list: {validated_emails_list}")
        return validated_emails_list

    def short(self, **mail_args):
        """
        Simply get the args to fill mail with to, cc, subject and text and send.
        https://docs.djangoproject.com/en/2.0/topics/email/

        :param mail_args: dict
        :return:
        """
        fake_run = mail_args.get('fake_run', False)
        mail_html = mail_args.get('mail_html', '')  # When nothing to render - send just plain text
        body = mail_args.get('body', False)  # When nothing to render - send just plain text
        subject = mail_args.get('subject', False)  # When nothing to render - send just plain text

        send_to = mail_args.get('send_to', 'email.service.error')  # Send to me, if None.
        send_cc = mail_args.get('send_cc', None)
        bcc = mail_args.get('bcc', None)

        send_to = self.get_group_or_user_recipients(send_to)
        send_cc = self.get_group_or_user_recipients(send_cc)
        bcc = self.get_group_or_user_recipients(bcc)

        images = mail_args.get('images', [])
        attach_file = mail_args.get('attach_file', '')
        attach_content = mail_args.get('attach_content', '')
        attach_content_name = mail_args.get('attach_content_name', 'draft.html')

        log.debug(f' send_to: {send_to} send_cc: {send_cc} bcc: {bcc}')
        assert isinstance(send_to, list), 'send_to should be a list!'
        assert isinstance(send_cc, list), 'send_cc should be a list!'
        assert isinstance(bcc, list), 'bcc should be a list!'

        txt = '{} {} host: {}'
        if not body and not mail_html:
            body = txt.format('No txt body added.', '\n', curr_hostname)
        else:
            body = "{} \n\t\tOn host: {}".format(body, curr_hostname)

        if not subject:
            subject = txt.format('No Subject added', ' - ', curr_hostname)

        # msg = f"subject: {subject} \n\tsend_to: {send_to} \n\tsend_cc: {send_cc} \n\tbcc: {bcc}"
        # if fake_run:
        #     # Fake run, but send email:
        #     log.debug(f'NOT Sending short email - FAKE RUN : \n\tsubject: {subject} \n\tsend_to: {send_to} \n\tsend_cc: {send_cc} \n\tbcc: {bcc}')
        #     mail_html_f = open(f'{subject}.html', 'w')
        #     mail_html_f.write(mail_html)
        #     mail_html_f.close()
        #     mail_html_f = open(f'attachment.html', 'w')
        #     mail_html_f.write(attach_content)
        #     mail_html_f.close()
        #     return f'Short mail sent! {msg}'
        # elif const.is_dev():
        #     # Probably a fake run, but on local dev - so do not send emails? Somehow this could be switchable, so I can test email locally!
        #     log.debug(f'NOT Sending short email settings.DEV: \n\tsubject: {subject} \n\tsend_to: {send_to} \n\tsend_cc: {send_cc} \n\tbcc: {bcc}')
        #     mail_html_f = open(f'{subject}.html', 'w')
        #     mail_html_f.write(mail_html)
        #     mail_html_f.close()
        #     mail_html_f = open(f'attachment.html', 'w')
        #     mail_html_f.write(attach_content)
        #     mail_html_f.close()
        #     return f'Short mail sent! {msg}'

        errs = []
        connection = mail.get_connection()
        # Try 3 times by default:
        for i in range(3):
            try:
                connection.open()
            except Exception as e:
                log.error(f"<=Mails short=> Try: {i} Cannot get email backend: {e}")
                errs.append(e)
                sleep(30)
            else:
                break
        else:
            log.critical(f'Cannot send email after 3 retries: {subject}. Exceptions collected: {errs}')
            return False

        email_args = dict(
            subject=subject,
            body=body,
            from_email=getattr(settings, 'EMAIL_ADDR', None),
            to=send_to,
            cc=send_cc,
            bcc=bcc,
            connection=connection,
        )
        # log.debug("<=MailSender=> short email_args - %s", email_args)
        if mail_html:
            # log.debug("<=MAIL SIMPLE=> Mail html send")
            email = EmailMultiAlternatives(**email_args)
            # log.debug("<=MailSender=> short email_args - %s", email_args)
            email.attach_alternative(mail_args.get('mail_html', ''), "text/html")
            if attach_file:
                email.attach_file(attach_file)
            if attach_content:
                email.attach(attach_content_name, attach_content, "text/html")

            iter_img = 0
            if images:
                for image in images:
                    iter_img += 1
                    stream = BytesIO()
                    image.save(stream, format="JPEG")
                    stream.seek(0)
                    imgObj = stream.read()
                    img = MIMEImage(imgObj)
                    img.add_header('Content-ID', '<image>')
                    email.attach(img)
            email.send()
        else:
            email = EmailMessage(**email_args)
            # log.debug("<=MailSender=> short email_args - %s", email_args)
            if attach_file:
                email.attach_file(attach_file)
            if attach_content:
                email.attach(attach_content_name, attach_content, "text/html")
            email.send()
            # log.debug("<=MAIL SIMPLE=> Mail txt send")

        # The connection was already open so send_messages() doesn't close it.
        # We need to manually close the connection.
        connection.close()
        return True
