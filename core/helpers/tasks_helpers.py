"""
Decorator and helpers for tasks, like:
- send emails on start/finish
- fix errors
- parse outputs, etc

"""
import functools
import json
# Python logger
import logging
import sys
import traceback
from pprint import pformat

from billiard.exceptions import WorkerLostError
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader

from core import constants as const

from core.helpers.mailing import Mails
from main.models import MailsTexts

log = logging.getLogger("core")
log_mail = logging.getLogger("mail")
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
            log_mail.error(f"Task exeption 'SoftTimeLimitExceeded': {e}")
            TMail().mail_log(function, e, _args=args, _kwargs=kwargs)
            return wrapper

        except TimeLimitExceeded as e:
            log.warning("Firing TimeLimitExceeded exception. Task will now die!")
            log_mail.error(f"Task exeption 'TimeLimitExceeded': {e}")
            TMail().mail_log(function, e, _args=args, _kwargs=kwargs)
            raise TimeLimitExceeded(e)

        except WorkerLostError as e:
            log_mail.error(f"Task exeption 'WorkerLostError': {e}")
            TMail().mail_log(function, e, _args=args, _kwargs=kwargs)
            raise Exception(e)

        except Exception as e:
            log.error(f"Unusual task exception! Check mail or logs for more info. {e}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            sam = traceback.format_exception(exc_type, exc_value, exc_traceback)
            exc_more = f'{e} Task catches the unusual exception. Please check logs or run debug. \n\t - Traceback: {sam}'
            TMail().mail_log(function, e, _args=args, _kwargs=kwargs, sam=sam)
            error_d = dict(
                function=function,
                error=sam,
                args=args,
                kwargs=kwargs,
            )
            log.error(f"Task Exception: {error_d}")
            try:
                item_sort = json.dumps(error_d, indent=2, ensure_ascii=False, default=pformat)
                log.error(f"Task Exception: {e} {item_sort}")
            except TypeError:
                log.error(f"Task Exception: {error_d}")
            if const.is_dev():
                log_mail.info(
                    f'Exceptions on test machine do not send mail log on task fail! {function} {exc_more} {args} {kwargs}')
                TMail().mail_log(function, e, _args=args, _kwargs=kwargs, sam=sam)
            raise Exception(e)

    return wrapper


def f_exception(function):
    """
    A decorator that wraps the passed in function and logs exceptions should one occur
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):

        try:
            return function(*args, **kwargs)

        except Exception as e:
            log.error(f"Unusual function exception! Check mail or logs for more info. {e}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            sam = traceback.format_exception(exc_type, exc_value, exc_traceback)
            exc_more = f'{e} Func catches the unusual exception. Please check logs or run debug. \n\t - Traceback: {sam}'
            TMail().mail_log(function, exc_more, _args=args, _kwargs=kwargs)
            error_d = dict(
                function=function,
                error=sam,
                args=args,
                kwargs=kwargs,
            )
            log.error(f"Func Exception: {error_d}")
            try:
                item_sort = json.dumps(error_d, indent=2, ensure_ascii=False, default=pformat)
                log.error(f"Func Exception: {e} {item_sort}")
            except TypeError:
                log.error(f"Func Exception: {error_d}")
            if const.is_dev():
                log.info(
                    f'Exceptions on test machine do not send mail log on task fail! {function} {exc_more} {args} {kwargs}')
                TMail().mail_log(function, exc_more, _args=args, _kwargs=kwargs)
            raise Exception(e)

    return wrapper


class TMail:

    def mail_log(self, function, e, _args, _kwargs, sam=None):
        send_to = _kwargs.get('user_name', False)
        if not send_to:
            send_to = _kwargs.get('user_email', 'email.service.error')

        # When something bad happened - use a selected text object to fill mail subject and body:
        log.error(f'<=TASK Exception mail_log=> Selecting mail txt for: "{function.__module__}.{function.__name__}"')
        try:
            mails_txt = MailsTexts.objects.get(mail_key__contains=f'{function.__module__}.{function.__name__}')
        except ObjectDoesNotExist:
            mails_txt = MailsTexts.objects.get(mail_key__contains='general_exception')

        subject = f'Exception: {mails_txt.subject} | {curr_hostname}'
        log.debug(f"<=TASK Exception mail_log=> Selected mail subject: {subject} send to: {send_to}")

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
