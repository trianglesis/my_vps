from __future__ import absolute_import, unicode_literals
import logging
from core import constants as const
from core.core_celery import app
from core.helpers.tasks_helpers import exception
from core.security import CeleryCreds
from main.visitors import save_visit, pick_request_useful_data
from main.models import Options
from core.security import Other

ADMIN_URL = Other.ADMIN_URL

log = logging.getLogger("dev")

@app.task(
    queue=CeleryCreds.QUEUE_CORE,
    routing_key='routines.MainTasks.make_snap',
    soft_time_limit=const.MIN_1, task_time_limit=const.MIN_1)
@exception
def t_save_visitor(request):
    save_visit(request)
    return True


def save_visit_task(request):
    # First get all we need from request (it's unpickable)
    data_pickable = pick_request_useful_data(request)

    r_path = data_pickable.get('path')
    # Do not save admin url requests
    if ADMIN_URL in r_path:
        return False

    # Skip-able paths list:
    skip_paths = Options.objects.get(option_key__exact='skip.request.paths')
    # If the option is True: skip
    if skip_paths.option_bool:
        skip_paths = eval(skip_paths.option_value)
        if any([True if path in r_path else False for path in skip_paths]):
            log.info(f"Path is skipable: {r_path}")
            return False

    # Now make actual work:
    task_added = t_save_visitor.apply_async(args=[data_pickable])
    log.info(f"Save visit task: {data_pickable.get('client_ip')} {data_pickable.get('path')} - {task_added}")
    return True
