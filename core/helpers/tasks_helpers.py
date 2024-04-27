"""
Decorator and helpers for tasks, like:
- send emails on start/finish
- fix errors
- parse outputs, etc

"""
import functools
# Python logger
import logging
import sys
import traceback

from billiard.exceptions import WorkerLostError
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader

from core.helpers.mailing import Mails
from main.models import MailsTexts

log = logging.getLogger("core")
curr_hostname = getattr(settings, 'CURR_HOSTNAME', None)


def exception(function):
    """
    A decorator that wraps the passed in function and logs exceptions should one occur
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):

        try:
            return function(*args, **kwargs)
        except SoftTimeLimitExceeded as e:
            log.warning("Firing SoftTimeLimitExceeded exception.")
            log.error(f"Task exception 'SoftTimeLimitExceeded': {e}")
            TMail().mail_log(function, e, _args=args, _kwargs=kwargs)
            return wrapper

        except TimeLimitExceeded as e:
            log.warning("Firing TimeLimitExceeded exception. Task will now die!")
            log.error(f"Task exception 'TimeLimitExceeded': {e}")
            TMail().mail_log(function, e, _args=args, _kwargs=kwargs)
            raise TimeLimitExceeded(e)

        except WorkerLostError as e:
            log.error(f"Task exception 'WorkerLostError': {e}")
            TMail().mail_log(function, e, _args=args, _kwargs=kwargs)
            raise Exception(e)

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            sam = traceback.format_exception(exc_type, exc_value, exc_traceback)
            log.error(f"Unusual task exception!"
                      f"\n\tCheck mail or logs for more info. "
                      f"\n\tfunction: {function}"
                      f"\n\targs: {args}"
                      f"\n\tkwargs: {kwargs}"
                      f"\n\tException: \n{e}"
                      f"\n\tTraceback: \n{sam}")
            # Last
            TMail().mail_log(function, e, _args=args, _kwargs=kwargs, sam=sam)
            raise Exception(e)

    return wrapper


class TMail:

    def mail_log(self, function, e, _args, _kwargs, sam=None):
        """
        Send email on task exception.
        Try next to taskify this.
        :param function:
        :param e:
        :param _args:
        :param _kwargs:
        :param sam:
        :return:
        """
        send_to = _kwargs.get('user_name', False)
        if not send_to:
            send_to = _kwargs.get('user_email', 'email.service.error')
        # When something bad happened - use a selected text object to fill mail subject and body:
        # Or create a new one with the default message.
        mails_txt = MailsTexts.objects.get_or_create(
            mail_key__contains=f'{function.__module__}.{function.__name__}',
            defaults={
                "subject": "General exception!",
                "description": "This is a general exception message, "
                               "it not a known exception, please investigate."
                               "\n\nUpdate this email body the backend site with later explanation.",
            }
        )
        subject = f'Exception: {mails_txt.subject} | {curr_hostname}'
        test_added = loader.get_template('helpers/exception_email.html')
        mail_html = test_added.render(dict(
            subject=subject,
            mails_txt=mails_txt,
            function_module=function.__module__,
            function_name=function.__name__,
            function_args=_args,
            function_kwargs=_kwargs,
            exception=e,
            exception_sam=sam,
        ))
        Mails().short(
            subject=subject,
            send_to=send_to,
            mail_html=mail_html,
            send_cc='email.service.error'
        )
        # return mail_html
        return True
