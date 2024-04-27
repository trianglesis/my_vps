import socket, sys

from core.security import HostnamesSupported, MySQLDatabase, RabbitMQCreds, DjangoCreds

hostname = socket.gethostname()

# 0 is DEV
# 1 is LIVE

ENV = 0
print("Setup credentials environment.")
if hostname == HostnamesSupported.DEV_HOSTNAME:
    ENV = 0
    print(f"Setup credentials Development: {hostname} ENV={ENV}")
elif hostname == HostnamesSupported.LIVE_HOSTNAME:
    ENV = 1
    print(f"Setup credentials Live: {hostname} ENV={ENV}")
else:
    print(f"ERROR: Setup credentials Unexpected: {hostname} ENV={ENV}")
    sys.exit(f"ERROR: Setup credentials Unexpected: {hostname} ENV={ENV}")


class MySQLCredentials:
    # Database
    ENGINE = MySQLDatabase.DB_ENGINE
    DB_NAME = MySQLDatabase.DB_NAME
    USER = MySQLDatabase.DB_USER
    PASSWORD = MySQLDatabase.DB_PASSWORD
    HOST = MySQLDatabase.DB_HOST
    PORT = MySQLDatabase.DB_PORT

    # Local Dev machine uses different IP
    if ENV == 0:
        HOST = MySQLDatabase.DB_HOST_WSL
        PASSWORD = MySQLDatabase.DB_HOST_WSL_PASSWD
        print(f"Setup credentials Use WSL networking to access local MySQL Database")


class Credentials:
    rabbitmq_user = RabbitMQCreds.RABBITMQ_USER
    rabbitmq_pswd = RabbitMQCreds.RABBITMQ_PSWD

    # Local Dev machine
    if ENV == 0:
        print(f"Setup credentials Development creds: {hostname} ENV={ENV}")
        HOSTNAME = HostnamesSupported.DEV_HOSTNAME
        FQDN = HostnamesSupported.DEV_FQDN
        IP = HostnamesSupported.DEV_IP
        HOSTEMAIL = HostnamesSupported.DEV_HOSTEMAIL
        SITE_SHORT_NAME = HostnamesSupported.DEV_SITE_SHORT_NAME
        EMAIL_HOST_USER = DjangoCreds.EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD = DjangoCreds.EMAIL_HOST_PASSWORD
        SITE = HostnamesSupported.DEV_WEB
        SITE_HTTP = HostnamesSupported.DEV_LIVE_WEB_HTML

    elif ENV == 1:
        print(f"Setup credentials Live creds: {hostname} ENV={ENV}")
        HOSTNAME = HostnamesSupported.LIVE_HOSTNAME
        FQDN = HostnamesSupported.LIVE_FQDN
        IP = HostnamesSupported.LIVE_IP
        HOSTEMAIL = HostnamesSupported.LIVE_HOSTEMAIL
        SITE_SHORT_NAME = HostnamesSupported.LIVE_SITE_SHORT_NAME
        EMAIL_HOST_USER = DjangoCreds.EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD = DjangoCreds.EMAIL_HOST_PASSWORD
        SITE = HostnamesSupported.LIVE_WEB
        SITE_HTTP = HostnamesSupported.LIVE_WEB_HTML
    else:
        print(f"ERROR: Setup credentials Unexpected creds: {hostname} ENV={ENV}")
        sys.exit(f"ERROR: Setup credentials Unexpected creds: {hostname} ENV={ENV}")
