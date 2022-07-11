"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import logging
import os
from pathlib import Path
import socket

from logging.config import dictConfig
import core.security

LOG_DIR = '/var/log/my_vps/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{asctime:<24}{levelname:<8}{filename:<20}{funcName:<22}L:{lineno:<6}{message:8s}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'django_dbug':
            {
                '()': 'core.helpers.log_filters.DebugDjangoFilters'
            },
    },
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + 'core.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 5,
        },
        'dev_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + 'dev.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 1,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'mail': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'core': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'dev': {
            'handlers': ['dev_log'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

dictConfig(LOGGING)

log = logging.getLogger("core")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = core.security.Credentials.SECRET_KEY
CURR_HOSTNAME = socket.getfqdn()

ALLOWED_HOSTS = ['localhost',
                 '127.0.0.1',
                 core.security.Credentials.SITE,
                 core.security.Credentials.SITE_IP,
                 core.security.Credentials.FQDN,
                 core.security.Credentials.WEB,
                 socket.getfqdn(),
                 socket.gethostname()
                 ]

CSRF_TRUSTED_ORIGINS = [
    "https://127.0.0.1",
    "https://localhost",
    f"https://{core.security.Credentials.FQDN}",
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEV = False

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django_registration',
    'main.apps.CoreConfig',
    'blog.apps.BlogConfig',
    'remotes.apps.RemotesConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'o_cache_table',
#         'TIMEOUT': 60 * 5,
#         'MAX_ENTRIES': 1000,
#         # 'KEY_FUNCTION': 'octo.helpers.cache_key.make_key',
#         # 'KEY_PREFIX': 'dev_o',
#     }
#     # 'default': {
#     #     'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
#     #     'LOCATION': '127.0.0.1:11211',
#     #     'TIMEOUT': 60 * 5,
#     #     'OPTIONS': {
#     #         'server_max_value_length': 1024 * 1024 * 10,
#     #     }
#     # }
# }


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / 'templates'],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Later ADD Mysql to:
DATABASES = {
    'default': {
        'ENGINE': core.security.Credentials.ENGINE,
        'NAME': core.security.Credentials.NAME,
        'USER': core.security.Credentials.USER,
        'PASSWORD': core.security.Credentials.PASSWORD,
        'HOST': core.security.Credentials.HOST,
        'PORT': core.security.Credentials.PORT,
        'CONN_MAX_AGE': 8000,
        'OPTIONS': {
            'read_default_file': '/etc/my.cnf',
            # 'read_default_file': '/etc/my.cnf.d/win_mysql.cnf',
            # 'init_command': 'SET default_storage_engine=INNODB;'
            # 'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
            # 'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(STATIC_ROOT, 'admin'),
)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://docs.djangoproject.com/en/2.0/topics/email/
EMAIL_HOST = core.security.Credentials.EMAIL_HOST
EMAIL_PORT = core.security.Credentials.EMAIL_PORT
EMAIL_HOST_USER = core.security.Credentials.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = core.security.Credentials.EMAIL_HOST_PASSWORD
EMAIL_SUBJECT_PREFIX = core.security.Credentials.EMAIL_SUBJECT_PREFIX
DEFAULT_FROM_EMAIL = core.security.Credentials.DEFAULT_FROM_EMAIL

# Mail addr:
EMAIL_ADDR = core.security.Credentials.HOSTEMAIL
SITE_DOMAIN = core.security.Credentials.FQDN
SITE_SHORT_NAME = core.security.Credentials.SITE_SHORT_NAME

# Django registration:
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True

# https://github.com/maxtepkeev/architect/issues/38
# https://github.com/celery/django-celery/issues/359
CONN_MAX_AGE = 8000

ADMINS = core.security.ADMINS

# ASGI_APPLICATION = "core.asgi.application"
