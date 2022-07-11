from __future__ import absolute_import, unicode_literals

import logging
from core.core_celery import app
from core import constants as const
from core.helpers.tasks_helpers import exception

log = logging.getLogger("celery")


class RemotesTasks:

    @staticmethod
    @app.task(queue='w_routines@tentacle.dq2', routing_key='routines.RemotesTasks.make_snap',
              soft_time_limit=const.MIN_5, task_time_limit=const.MIN_5)
    @exception
    def make_snap(t_tag, **kwargs):
        log.info("This is my first task!")
