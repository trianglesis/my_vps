from __future__ import absolute_import, unicode_literals

import logging

from core.core_celery import app
from core import constants as const
from core.helpers.tasks_helpers import exception
from core.security import CeleryCreds

log = logging.getLogger("core")


class CoreTasks:

    @staticmethod
    @app.task(
        queue=CeleryCreds.QUEUE_CORE,
        routing_key='routines.CoreTasks.core_task',
        soft_time_limit=const.MIN_5, task_time_limit=const.MIN_5)
    @exception
    def core_task(t_tag, **kwargs):
        log.info(f"This is my first core  task! {t_tag}, {kwargs}")
