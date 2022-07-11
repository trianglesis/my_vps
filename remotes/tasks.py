from __future__ import absolute_import, unicode_literals

import logging

from celery.schedules import crontab

from core.core_celery import app
from core import constants as const
from core.helpers.tasks_helpers import exception

log = logging.getLogger("celery")


app.conf.beat_schedule = {
    # Run MAIN for each working day till 20th:
    'tkn_main_workday_routine': {
        'task': 'remotes.tasks.RemotesTasks.make_snap',
        'schedule': crontab(hour=17, minute=0, day_of_week='1,2,3,4,5', day_of_month='1-19,28-31'),
        'options': {'queue': 'routines'},
        'args': ('tkn_main',),
        'kwargs': {'send_mail': True, 'sync_tku': True, 'user_name': 'cron_user'},
    },
}


class RemotesTasks:

    @staticmethod
    @app.task(routing_key='routines.RemotesTasks.make_snap', soft_time_limit=const.MIN_5, task_time_limit=const.MIN_5)
    @exception
    def make_snap(t_tag, **kwargs):
        log.info("This is my first task!")
