from __future__ import absolute_import, unicode_literals
import logging
from core import constants as const
from core.core_celery import app
from core.helpers.tasks_helpers import exception
from core.security import CeleryCreds
from main.visitors import save_visit, pick_request_useful_data
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
    # Do not save admin url requests
    if ADMIN_URL in data_pickable.get('path'):
        return False
    # Now make actual work:
    task_added = t_save_visitor.apply_async(args=[data_pickable])
    log.info(f"Save visit task: {data_pickable.get('client_ip')} {data_pickable.get('path')} - {task_added}")
    return True
