from __future__ import absolute_import, unicode_literals

import logging

from core import constants as const
from core.core_celery import app
from core.helpers.tasks_helpers import exception
from core.security import QueuesCelery
from remotes.routines import make_snap_send_email_routine

log = logging.getLogger("core")


class RemotesTasks:

    @staticmethod
    @app.task(
        queue=QueuesCelery.QUEUE_REMOTES,
        routing_key='routines.RemotesTasks.make_snap',
        soft_time_limit=const.MIN_5, task_time_limit=const.MIN_5)
    @exception
    def t_make_snap_on_open(t_tag, **kwargs):
        log.info(f"Making snap on: {t_tag}, kwargs: {kwargs}")
        tasking = make_snap_send_email_routine(**kwargs)
        return tasking
