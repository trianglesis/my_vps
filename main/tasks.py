from __future__ import absolute_import, unicode_literals

import logging

from core import constants as const
from core.core_celery import app
from core.helpers.mailing import Mails
from core.helpers.tasks_helpers import exception
from core.security import CeleryCreds, DjangoCreds
from core.security import Other
from main.models import Options
from main.visitors import skip, save_visit, pick_request_useful_data
from blog.calculations import calculate_hits

ADMIN_URL = Other.ADMIN_URL

log = logging.getLogger("core")


@app.task(
    queue=CeleryCreds.QUEUE_CORE,
    routing_key='main.t_save_visitor',
    soft_time_limit=const.MIN_1, task_time_limit=const.MIN_1)
@exception
def t_save_visitor(request, **kwargs):
    """
    Save request data from any HTTP Request visit
    :param request:
    :return:
    """
    save_visit(request, **kwargs)
    return True


@app.task(
    queue=CeleryCreds.QUEUE_CORE,
    routing_key='main.t_calculate_hits',
    soft_time_limit=const.MIN_1, task_time_limit=const.MIN_1)
@exception
def t_calculate_hits():
    """
    Calculate posts visitors, once a day.
    :return:
    """
    calculate_hits()
    return True


@app.task(
    queue=CeleryCreds.QUEUE_CORE,
    routing_key='main.t_raise_exception',
    soft_time_limit=const.MIN_1, task_time_limit=const.MIN_1)
@exception
def t_raise_exception(*args, **kwargs):
    msg = (f"Task for exception!"
           f"\n\targs: {args}"
           f"\n\tkwargs: {kwargs}")
    log.error(msg)
    try:
        Mails().short(
            subject="t_raise_exception",
            body=msg,
            send_to=DjangoCreds.mails['admin'],
            bcc=DjangoCreds.mails['admin']
        )
    except Exception as e:
        log.error(f"Task for exception cannot send a test email!"
                  f"\n\tException:\n{e}")

    raise Exception(msg)


def save_visit_task(request, status=None):
    """
    Save user visit with useful request data.
    Skip local paths, IPs, admin views, and so on.
    :param request:
    :return:
    """
    # First get all we need from request (it's unpickable)
    data_pickable = pick_request_useful_data(request)

    # Do not save admin url requests
    if ADMIN_URL in data_pickable.get('path'):
        return False

    show_log = Options.objects.get(option_key__exact='save_visit_task.log_info').option_bool

    # Variants that we don't want to save:
    if skip('skip.request.paths', data_pickable.get('path'), show_log):
        return False
    if skip('skip.client_ip', data_pickable.get('client_ip'), show_log):
        return False
    if skip('skip.user_agent', data_pickable.get('u_agent'), show_log):
        return False

    # For dev ENV just run as it is
    if const.is_dev():
        log.warning(f"Non TASK save request at DEV ENV!"
                    f"\n\tPath: {data_pickable['path']}"
                    f"\n\tStatus: {status}"
                    f"")
        save_visit(data_pickable, status=status, show_log=show_log)
    # Now make actual work:
    else:
        task_added = t_save_visitor.apply_async(args=[data_pickable], kwargs=dict(status=status, show_log=show_log))
        if show_log:
            log.info(f"Save visit task: {data_pickable.get('client_ip')} {data_pickable.get('path')} - {task_added}")
    return True
