from __future__ import absolute_import, unicode_literals

import logging

from celery.schedules import crontab

from core.core_celery import app
from core import constants as const
from core.helpers.tasks_helpers import exception

log = logging.getLogger("celery")

app.conf.beat_schedule = {
    # Run MAIN for each working day till 20th:
    'core_init_task': {
        'task': 'core.tasks.CoreTasks.core_task',
        'schedule': crontab(hour=17, minute=0, day_of_week='1,2,3,4,5', day_of_month='1-19,28-31'),
        'options': {'queue': 'core@layer.dq2'},
        'args': ('dummy',),
        'kwargs': {'send_mail': True, 'spam': True, 'user_name': 'cron_user'},
    },
}


class CoreTasks:

    @staticmethod
    @app.task(
        queue='core@layer.dq2',
        routing_key='routines.CoreTasks.core_task',
        soft_time_limit=const.MIN_5, task_time_limit=const.MIN_5)
    @exception
    def core_task(t_tag, **kwargs):
        log.info(f"This is my first core  task! {t_tag}, {kwargs}")

    @app.task()
    def test_task(self):
        log.info('This is test task!')
