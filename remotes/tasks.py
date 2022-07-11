from __future__ import absolute_import, unicode_literals

import logging
from core.core_celery import app
from core import constants as const
from core.helpers.tasks_helpers import exception
from core.security import QueuesCelery, Credentials, mails

from core.helpers.mailing import Mails

log = logging.getLogger("core")


class RemotesTasks:

    @staticmethod
    @app.task(
        queue=QueuesCelery.QUEUE_REMOTES,
        routing_key='routines.RemotesTasks.make_snap',
        soft_time_limit=const.MIN_5, task_time_limit=const.MIN_5)
    @exception
    def t_make_snap_on_open(t_tag, **kwargs):
        username = kwargs.get('username')
        send_to = kwargs.get('send_to')
        camera_shot = kwargs.get('camera_shot')
        button = kwargs.get('button')
        perl_hostname = kwargs.get('perl_hostname')
        image_enhance = kwargs.get('image_enhance')
        mail_html = kwargs.get('mail_html')

        subject = f'Remote snapshot: {button.description}'
        log.info(f"Run make_snap for user: {username} tag: {t_tag}")

        images = camera_shot(button, perl_hostname, image_enhance)

        Mails().short(
            subject=subject,
            mail_html=mail_html,
            images=images,
            send_to=send_to,
            bcc=mails['admin'],
        )
