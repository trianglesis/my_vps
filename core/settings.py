"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import logging
import os, sys
from pathlib import Path
import socket

from logging.config import dictConfig

from core.setup_logic import Credentials, MySQLCredentials
from core.security import DjangoCreds, HostnamesSupported

hostname = socket.gethostname()

ENV = 0
print("Settings: Setup settings environment.")
if hostname == HostnamesSupported.DEV_HOSTNAME:
    ENV = 0
    LOG_DIR = 'x_logs'
    DEBUG = True
    DEV = True
    THIS_IS_DEV = True
    print(f"Settings: Development: {hostname} ENV={ENV}")
elif hostname == HostnamesSupported.LIVE_HOSTNAME:
    ENV = 1
    # SECURITY WARNING: don't run with debug turned on in production!
    DEV = False
    DEBUG = False
    LOG_DIR = '/var/log/my_vps/'
    print(f"Settings: Live: {hostname} ENV={ENV}")
else:
    print(f"ERROR: Settings Unexpected: {hostname} ENV={ENV}")
    sys.exit(f"ERROR: Settings Unexpected: {hostname} ENV={ENV}")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{asctime:<24s}[{levelname:-<7s}{name:->7s}]{module:>30s}:{funcName:<30s}:{lineno:<5d}{message}',
            'style': '{',
        },
        'console_view': {
            'format': '{asctime:<24s}[{levelname:-<7s}{name:->7s}]{module:>30s}:{funcName:<30s}:{lineno:<5d}{message}',
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
        # 'django_dbug':
        #     {
        #         '()': 'core.helpers.log_filters.DebugDjangoFilters'
        #     },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true', ],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # the email message it sends will contain a full traceback, with names and values of local variables at each level
            'include_html': False,
            # 'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'core.log'),
            'formatter': 'verbose',
        },
        'celery': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'celery.log'),
            'formatter': 'verbose',
        },
        'dev_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'dev.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'celery': {
            'handlers': ['celery'],
            'level': 'INFO',
            'propagate': False
        },
        'mail': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'core': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'dev': {
            'handlers': ['dev_log'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# If debug
if DEBUG:
    print(f"Settings: WSL: Use email logs for errors.")
    LOGGING['handlers']['mail_admins'] = {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
        # the email message it sends will contain a full traceback, with names and values of local variables at each level
        'include_html': True
    }

# For local development
if ENV == 0:
    print(f"Settings: WSL: Redirect all logs to console output with simple format.")
    LOGGING['disable_existing_loggers'] = False
    # Add console:
    LOGGING['handlers']['console']['formatter'] = 'console_view'
    # All levels to debug:
    LOGGING['handlers']['console']['level'] = 'DEBUG'
    # All handlers to console:
    LOGGING['loggers']['django']['handlers'].append('console')
    LOGGING['loggers']['celery']['handlers'].append('console')
    LOGGING['loggers']['mail']['handlers'].append('console')
    LOGGING['loggers']['core']['handlers'].append('console')
    LOGGING['loggers']['dev']['handlers'].append('console')
    # All to debug:
    LOGGING['loggers']['django']['level'] = "INFO"
    LOGGING['loggers']['celery']['level'] = "DEBUG"
    LOGGING['loggers']['mail']['level'] = "DEBUG"
    LOGGING['loggers']['core']['level'] = "DEBUG"
    LOGGING['loggers']['dev']['level'] = "DEBUG"

dictConfig(LOGGING)
log = logging.getLogger("core")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DjangoCreds.SECRET_KEY
CURR_HOSTNAME = socket.getfqdn()

ALLOWED_HOSTS = ['localhost',
                 '127.0.0.1',
                 Credentials.FQDN,
                 Credentials.IP,
                 Credentials.HOSTNAME,
                 HostnamesSupported.LIVE_IPV6,
                 HostnamesSupported.LIVE_WEB,
                 HostnamesSupported.LIVE_WEB_WWW,
                 socket.getfqdn(),
                 socket.gethostname()
                 ]

CSRF_TRUSTED_ORIGINS = [
    "https://127.0.0.1",
    "https://localhost",
    f"https://{Credentials.FQDN}",
    f"https://{Credentials.IP}",
    f"https://{HostnamesSupported.LIVE_WEB}",
]

CORS_ALLOWED_ORIGINS = [
    "https://127.0.0.1",
    "https://localhost",
    f"https://{Credentials.FQDN}",
    f"https://{Credentials.IP}",
    f"https://{HostnamesSupported.LIVE_WEB}",
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# In local dev
if ENV == 0:
    CSRF_TRUSTED_ORIGINS.extend([
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "http://localhost",
        "http://localhost:8000",
    ])
    INTERNAL_IPS.extend(ALLOWED_HOSTS)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat.apps.BeatConfig',
    # 'dj_rest_auth',
    'django_registration',
    'core',
    'main.apps.CoreConfig',
    'blog.apps.BlogConfig',
    'remotes.apps.RemotesConfig',
    'tinymce',
]

SITE_ID = 1

# In local dev
if ENV == 0:
    INSTALLED_APPS.extend([
        # 'channels',
        # 'corsheaders',
        'debug_toolbar',
    ])

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'main.middleware.UserVisitMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

# Local DEV and Lobster and New Octopus?
if ENV == 0:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOWED_ORIGINS = [
        f"http://{Credentials.FQDN}",
        "http://localhost",
        "http://localhost:80",
        "http://localhost:8080",
        "http://localhost:8000",
    ]

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'o_cache_table',
#         'TIMEOUT': 60 * 5,
#         'MAX_ENTRIES': 1000,
#         # 'KEY_FUNCTION': 'core.helpers.cache_key.make_key',
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
        'ENGINE': MySQLCredentials.ENGINE,
        'NAME': MySQLCredentials.DB_NAME,
        'USER': MySQLCredentials.USER,
        'PASSWORD': MySQLCredentials.PASSWORD,
        'HOST': MySQLCredentials.HOST,
        'PORT': MySQLCredentials.PORT,
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

if ENV == 0:
    # noinspection PyUnresolvedReferences
    STATIC_ROOT = '//mnt//d//Projects//PycharmProjects//my_vps//static'
    # Win have different static logic
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),  # AT WSL2 this should be active
        os.path.join(os.path.join(BASE_DIR, 'static'), 'octicons'),
        os.path.join(os.path.join(BASE_DIR, 'static'), 'favicon'),
        os.path.join(os.path.join(BASE_DIR, 'static'), 'admin'),
        os.path.join(os.path.join(BASE_DIR, 'static'), 'core'),
        os.path.join(os.path.join(BASE_DIR, 'static'), 'remotes'),
    )
    STATIC_URL = '/static/'
    print(f"Settings: WSL: STATICFILES_DIRS: {STATICFILES_DIRS}")
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = (
        os.path.join(STATIC_ROOT, 'admin'),
    )
    STATIC_URL = '/static/'
    print(f"Settings: Live: STATICFILES_DIRS: {STATICFILES_DIRS}")

# Tiny MCE https://www.tiny.cloud/my-account/integrate/#more
# Buttons https://www.tiny.cloud/docs/advanced/available-toolbar-buttons/
# Only for cloud!
# TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/id2tbcpsi0fidqs5ntnru0azxgsoyrf96hrkkvnee5osbmvb/tinymce/7/tinymce.min.js'
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": "620px",
    "width": "1260px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code "
               "fullscreen insertdatetime media table code help wordcount codesample",
    # https://www.tiny.cloud/docs/tinymce/6/available-toolbar-buttons/
    "toolbar1": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
                "aligncenter alignright alignjustify | outdent indent | numlist bullist checklist | forecolor "
                "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
                "fullscreen preview save print | insertfile image media pageembed template link anchor | "
                "a11ycheck ltr rtl | showcomments addcomment",
    "toolbar2": "codesample | h1 h2 h3 h4 h5 h6 | code ",
    # "toolbar3": "table tablecellprops tablecopyrow tablecutrow tabledelete tabledeletecol tabledeleterow "
    #             "tableinsertdialog tableinsertcolafter tableinsertcolbefore tableinsertrowafter tableinsertrowbefore "
    #             "tablemergecells tablepasterowafter tablepasterowbefore tableprops tablerowprops tablesplitcells "
    #             "tableclass tablecellclass tablecellvalign tablecellborderwidth tablecellborderstyle tablecaption "
    #             "tablecellbackgroundcolor tablecellbordercolor tablerowheader tablecolheader",
    "custom_undo_redo_levels": 10,
    "codesample_global_prismjs": True,
    "codesample_languages": [
        {'value': "py", 'text': "Python"},
        {'value': "sh", 'text': "Shell .sh"},
        {'value': "bash", 'text': "BASH"},
        {'value': "shell-session", 'text': "shell-session"},
        {'value': "json", 'text': "JSON"},
        {'value': "html", 'text': "HTML"},
        {'value': "xml", 'text': "XML"},
        {'value': "yaml", 'text': "YAML .yaml"},
        {'value': "yml", 'text': "YAML .yml"},
        {'value': "django", 'text': "Django/Jinja2"},
        {'value': "editorconfig", 'text': "EditorConfig"},
        {'value': "ini", 'text': "ini"},
        {'value': "apacheconf", 'text': "Apache Configuration"},
        {'value': "csv", 'text': "CSV"},
        {'value': "graphql", 'text': "GraphQL"},
        {'value': "http", 'text': "HTTP"},
        {'value': "gitignore", 'text': ".gitignore"},
        {'value': "git", 'text': ".git"},
        {'value': "JavaScript", 'text': "javascript"},
        {'value': "CSS", 'text': "css"},
        {'value': "log", 'text': "Log file .log"},
        {'value': "md", 'text': "Markdown .md"},
        {'value': "nginx", 'text': "nginx"},
        {'value': "powershell", 'text': "PowerShell"},
        {'value': "sh-session", 'text': "sh-session"},
        {'value': "shellsession", 'text': "shellsession"},
        {'value': "sql", 'text': "SQL"},
        {'value': "systemd", 'text': "Systemd configuration file"},
        {'value': "vim", 'text': "vim"},
        {'value': "wiki", 'text': "Wiki markup"},
        {'value': "makefile", 'text': "makefile"},
        {'value': "python", 'text': "Python"},
    ],

}

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

SESSION_COOKIE_AGE = 60 * 60 * 24 * 120  # 4 months

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# https://docs.djangoproject.com/en/2.0/topics/email/
EMAIL_HOST = DjangoCreds.EMAIL_HOST
EMAIL_PORT = DjangoCreds.EMAIL_PORT
EMAIL_HOST_USER = DjangoCreds.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = DjangoCreds.EMAIL_HOST_PASSWORD
EMAIL_SUBJECT_PREFIX = DjangoCreds.EMAIL_SUBJECT_PREFIX
DEFAULT_FROM_EMAIL = DjangoCreds.DEFAULT_FROM_EMAIL

# Mail addr:
EMAIL_ADDR = Credentials.HOSTEMAIL
SITE_DOMAIN = Credentials.FQDN
SITE_SHORT_NAME = Credentials.SITE_SHORT_NAME

# Django registration:
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True

# https://github.com/maxtepkeev/architect/issues/38
# https://github.com/celery/django-celery/issues/359
CONN_MAX_AGE = 300

ADMINS = DjangoCreds.ADMINS

# ASGI_APPLICATION = "core.asgi.application"
