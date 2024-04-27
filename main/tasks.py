from __future__ import absolute_import, unicode_literals

import logging

from core import constants as const
from core.core_celery import app
from core.helpers.mailing import Mails
from core.helpers.tasks_helpers import exception
from core.security import CeleryCreds, DjangoCreds
from core.security import Other
from main.models import Options
from main.visitors import save_visit, pick_request_useful_data
from blog.calculations import calculate_hits

ADMIN_URL = Other.ADMIN_URL

log = logging.getLogger("core")


@app.task(
    queue=CeleryCreds.QUEUE_CORE,
    routing_key='main.t_save_visitor',
    soft_time_limit=const.MIN_1, task_time_limit=const.MIN_1)
@exception
def t_save_visitor(request):
    """
    Save request data from any HTTP Request visit
    :param request:
    :return:
    """
    save_visit(request)
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


def save_visit_task(request):
    """
    Save user visit with useful request data.
    Skip local paths, IPs, admin views, and so on.
    :param request:
    :return:
    """
    # First get all we need from request (it's unpickable)
    data_pickable = pick_request_useful_data(request)

    r_path = data_pickable.get('path')
    # Do not save admin url requests
    if ADMIN_URL in r_path:
        return False

    show_log = Options.objects.get(option_key__exact='save_visit_task.log_info').option_bool
    # Skip-able paths list:
    skip_paths = Options.objects.get(option_key__exact='skip.request.paths')
    # If the option is True: skip
    if skip_paths.option_bool:
        #  TODO: Validate and catch
        skip_paths = eval(skip_paths.option_value)
        if any([True if path in r_path else False for path in skip_paths]):
            if show_log:
                log.info(f"Path is skip able: {r_path}")
            return False

    client_ip = data_pickable.get('client_ip')
    skip_ips = Options.objects.get(option_key__exact='skip.client_ip')
    # If the option is True: skip
    if skip_ips.option_bool:
        # TODO: Validate and catch
        skip_ips = eval(skip_ips.option_value)
        if any(client_ip == ip for ip in skip_ips):
            if show_log:
                log.info(f"IP is skip able: {client_ip}")
            return False

    # For dev ENV just run as it is
    if const.is_dev():
        log.warning(f"Non TASK save request at DEV ENV!")
        save_visit(data_pickable)
    # Now make actual work:
    else:
        task_added = t_save_visitor.apply_async(args=[data_pickable])
        if show_log:
            log.info(f"Save visit task: {data_pickable.get('client_ip')} {data_pickable.get('path')} - {task_added}")
    return True
