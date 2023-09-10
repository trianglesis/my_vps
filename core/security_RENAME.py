HOSTNAME = 'HOSTNAME'
DEV_HOST = 'LOCAL_DEV_HOSTNAME'

VPS = 'HOSTNAME.VPS.net'


class QueuesCelery:
    QUEUE_MAIN = "default"
    # QUEUE_CORE = "core@layer.dq2"
    QUEUE_CORE = "default"
    # QUEUE_REMOTES = "remotes@layer.dq2"
    QUEUE_REMOTES = "default"


class Credentials:
    DEV_HOST = 'LOCAL_DEV_HOSTNAME'

    # SITE = 'WEB_FQDN'
    SITE = 'LOCAL_DEV_HOSTNAME'
    SITE_IP = 'REMOTE_IP'
    SECRET_KEY = 'KEY'

    ENGINE = 'django.db.backends.mysql'
    NAME = '__DB_NAME__'
    USER = '__DB_USER__'
    PASSWORD = '__DB_PASSWORD__'
    # HOST = 'localhost'
    HOST = '127.0.0.1'
    PORT = '3306'

    PASSWORD_LOCAL = '__DB_USER__'

    EMAIL_HOST = 'mail.adm.tools'
    EMAIL_PORT = '25'
    EMAIL_HOST_USER = 'no-reply@SITE_FQDN'
    DEFAULT_FROM_EMAIL = 'no-reply@SITE_FQDN'

    EMAIL_HOST_PASSWORD = '4diGzvPXU$5!zb'

    EMAIL_SUBJECT_PREFIX = '[Trianglesis] '

    # Local
    HOSTNAME = 'LOCAL_DEV_HOSTNAME'
    FQDN = '127.0.0.1:8000'
    HOSTEMAIL = 'to@SITE_FQDN'
    SITE_SHORT_NAME = 'Local'

    # External
    # HOSTNAME = 'HOSTNAME'
    # FQDN = 'HOSTNAME.VPS.net'
    # WEB = 'WEB_FQDN'
    # # HOSTEMAIL = 'HOSTNAME@SITE_FQDN'
    # HOSTEMAIL = 'no-reply@SITE_FQDN'
    # SITE_SHORT_NAME = 'core'

    # Site domain:
    LOCAL = 'LOCAL_DEV_HOSTNAME'
    LIVE = 'HOSTNAME'

    # Future RabbitMQ
    broker = 'pyamqp://__USER_RABBITMQ__:__PASSWORD__@localhost:5672/layer'
    # Future MySQL Backend for Celery
    backend = 'db+mysql://__USER_CELERY__:__PASSWORD__@localhost/__DB_NAME__'
    # Future MySQL Backend for my_vps
    result_backend = 'db+mysql://__USER_CELERY__:__PASSWORD__@localhost/__DB_NAME__'

    # wsl_backend='file:///opt/celery/',
    # wsl_result_backend='file:///opt/celery/',
    wsl_backend = 'db+mysql://__USER_CELERY__:__PASSWORD__@127.0.0.1/__DB_NAME__'
    wsl_result_backend = 'db+mysql://__USER_CELERY__:__PASSWORD__@127.0.0.1/__DB_NAME__'

    rabbitmq_url = 'amqp://__USER_RABBITMQ__:__PASSWORD__@localhost:5672/layer'
    rabbitmq_user = '__USER_RABBITMQ__'
    rabbitmq_pswd = '__PASSWORD__'


mails = dict(
    admin='EMAIL@EMAIL',

)

ADMINS = [
    ('USER', 'EMAIL@EMAIL'),
    ('to_USER', 'to@SITE_FQDN'),
]
