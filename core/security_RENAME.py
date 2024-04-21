class HostnamesSupported:
    # Live
    LIVE_HOSTNAME = 'vps-000000'
    LIVE_FQDN = 'vps-000000.hostname.org'
    LIVE_HOSTEMAIL = 'vps-000000@site.com'
    LIVE_IP = '1.2.3.4'
    LIVE_WEB = 'vps.site.com'
    LIVE_SITE_SHORT_NAME = 'core'
    # Local
    DEV_HOSTNAME = 'local-pc'
    DEV_FQDN = '127.0.0.1:8000'
    DEV_HOSTEMAIL = 'to@site.com'
    DEV_IP = '127.0.0.1'
    DEV_WEB = '127.0.0.1'
    DEV_SITE_SHORT_NAME = 'Local'


class DjangoCreds:
    SECRET_KEY = 'SECRET'
    EMAIL_HOST = 'some.mail.com'
    EMAIL_PORT = '25'
    EMAIL_HOST_USER = 'no-reply@site.com'
    EMAIL_HOST_PASSWORD = 'PASS'
    EMAIL_SUBJECT_PREFIX = '[PREFIX] '
    DEFAULT_FROM_EMAIL = 'no-reply@site.com'
    mails = dict(
        admin='email@email.com',
    )
    ADMINS = [
        ('sanek', 'email@email.com'),
        ('to_sanek', 'to@site.com'),
    ]


class MySQLDatabase:
    DB_ENGINE = 'django.db.backends.mysql'
    DB_USER = 'core_db'
    DB_HOST = 'localhost'
    DB_PORT = '3306'
    # Live and DEV versions
    DB_NAME = 'my_vps'
    DB_PASSWORD = 'PASSWORD'
    # Local development use WSL IP!
    DB_HOST_WSL = '192.168.127.254'
    DB_HOST_WSL_PASSWD = 'PASSWORD'


class RabbitMQCreds:
    RABBITMQ_USER = 'USER'
    RABBITMQ_PSWD = 'PASSWORD'
    BROKER = f'pyamqp://{RABBITMQ_USER}:{RABBITMQ_PSWD}@localhost:5672/layer'
    RABBITMQ_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PSWD}@localhost:5672/layer'


class CeleryCreds:
    DB_HOST = 'localhost'
    DB_HOST_Win = '127.0.0.1'
    DB_HOST_WSL = '192.168.127.254'

    DB_USER = 'celery'
    DB_PASSWORD = 'PASSWORD'

    BACKEND = 'db+mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    RESULT_BACKEND = 'db+mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

    QUEUE_MAIN = "default"
    # QUEUE_CORE = "core@layer.dq2"
    QUEUE_CORE = "default"
    # QUEUE_REMOTES = "remotes@layer.dq2"
    QUEUE_REMOTES = "default"

    WORKERS = ["core@layer",
               "remotes@layer",
               ]
    WSL_WORKERS = ["core@layer",
                   "remotes@layer",
                   ]


class Other:

    GOOGLE_ANALYTICS_ID = 'TOKEN'
    ADMIN_URL = "FAKE_URL_PATH"