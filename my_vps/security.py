"""
!!!WARNING!!!
!!!WARNING!!!
!!!WARNING!!!

THIS FILE SHOULD NEVER BE UPDATED TO ACTUAL INFORMATION AND NEVER TRACKED BUT VERSION CONTROL SYSTEM!

THIS IS DRAFT - IT LATER WILL BE IGNORED!

!!!WARNING!!!
!!!WARNING!!!
!!!WARNING!!!
"""

DEV_HOST = 'LOCAL_HOSTNAME'


class Credentials:
    SECRET_KEY = 'SECRET_KEY'
    ENGINE = 'django.db.backends.mysql'
    NAME = 'DATABASE_NAME'
    USER = 'DATABASE_USER'
    PASSWORD = 'DATABASE_PASSWORD'
    HOST = '127.0.0.1'
    PORT = '3306'

    EMAIL_HOST = 'EMAIL_HOST'

    # Local
    HOSTNAME = 'LOCAL_HOSTNAME'
    FQDN = '127.0.0.1:8000'
    HOSTEMAIL = 'local@local.com'
    SITE_SHORT_NAME = 'Local'

    # External
    # HOSTNAME = 'vps-40848'
    # FQDN = 'vps-40848'
    # HOSTEMAIL = 'vps-40848@trianglesis.org.ua'
    # SITE_SHORT_NAME = 'my_vps'

    # Site domain:
    LOCAL = 'LOCAL_HOSTNAME'
    LIVE = 'vps-40848'

    # Future RabbitMQ
    broker = 'pyamqp://USERNAME:PASSWORD@localhost:5672/workes_group_name'
    # Future MySQL Backend for Celery
    backend = 'db+mysql://USER_NAME:PASSWORD@localhost/DATABASE_NAME'
    # Future MySQL Backend for Celery
    result_backend = 'db+mysql://USER_NAME:PASSWORD@localhost/DATABASE_NAME'

    # wsl_backend='file:///opt/celery/',
    # wsl_result_backend='file:///opt/celery/',
    wsl_backend = 'db+mysql://USER_NAME:PASSWDS@127.0.0.1/DATABASE'
    wsl_result_backend = 'db+mysql://USER_NAME:PASSWDS@127.0.0.1/DATABASE'

    rabbitmq_url = 'amqp://USERNAME:PASSWORD@localhost:5672/workes_group_name'
    rabbitmq_user = 'USERNAME'
    rabbitmq_pswd = 'PASSWORD'


mails = dict(
    admin='PUBLICEMAIL',

)


ADMINS = [
    ('sanek', 'PUBLICEMAIL'),
    ('to_sanek', 'LOCALEMAIL'),
]


"""
!!!WARNING!!!
!!!WARNING!!!
!!!WARNING!!!

THIS FILE SHOULD NEVER BE UPDATED TO ACTUAL INFORMATION AND NEVER TRACKED BUT VERSION CONTROL SYSTEM!

THIS IS DRAFT - IT LATER WILL BE IGNORED!

!!!WARNING!!!
!!!WARNING!!!
!!!WARNING!!!
"""
