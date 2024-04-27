from __future__ import absolute_import, unicode_literals

import os
import socket
import sys

import django
from celery import Celery
from kombu import Exchange

from core.security import CeleryCreds, HostnamesSupported, RabbitMQCreds, MySQLDatabase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

hostname = socket.gethostname()

# 0 is DEV
# 1 is Live
ENV = 0
print("Celery initialization.")
if hostname == HostnamesSupported.DEV_HOSTNAME:
    ENV = 0
    DB_NAME = MySQLDatabase.DB_NAME
    workers = CeleryCreds.WORKERS
    print(f"Celery Development: {hostname} ENV={ENV}")
elif hostname == HostnamesSupported.LIVE_HOSTNAME:
    ENV = 1
    DB_NAME = MySQLDatabase.DB_NAME
    workers = CeleryCreds.WORKERS
    print(f"Celery Live: {hostname} ENV={ENV}")
else:
    print(f"ERROR: Celery Unexpected: {hostname} ENV={ENV}")
    sys.exit(f"ERROR: Celery Unexpected: {hostname} ENV={ENV}")

# WSL Options only
if ENV == 0:
    backend = CeleryCreds.BACKEND.format(
        DB_USER=CeleryCreds.DB_USER,
        DB_PASSWORD=CeleryCreds.DB_PASSWORD,
        DB_HOST=CeleryCreds.DB_HOST_WSL,
        DB_NAME=DB_NAME,
    )
    result_backend = CeleryCreds.RESULT_BACKEND.format(
        DB_USER=CeleryCreds.DB_USER,
        DB_PASSWORD=CeleryCreds.DB_PASSWORD,
        DB_HOST=CeleryCreds.DB_HOST_WSL,
        DB_NAME=DB_NAME,
    )
    print(f"Celery WSL: {CeleryCreds.DB_HOST_WSL}")
    print(f"Celery WSL backend: {backend}")
    print(f"Celery WSL result_backend: {result_backend}")
else:
    backend = CeleryCreds.BACKEND.format(
        DB_USER=CeleryCreds.DB_USER,
        DB_PASSWORD=CeleryCreds.DB_PASSWORD,
        DB_HOST=CeleryCreds.DB_HOST,
        DB_NAME=DB_NAME,
    )
    result_backend = CeleryCreds.RESULT_BACKEND.format(
        DB_USER=CeleryCreds.DB_USER,
        DB_PASSWORD=CeleryCreds.DB_PASSWORD,
        DB_HOST=CeleryCreds.DB_HOST,
        DB_NAME=DB_NAME,
    )

# Setup django project
django.setup()
#  The backend is specified via the backend argument to Celery
app = Celery('core',
             # http://docs.celeryproject.org/en/latest/userguide/optimizing.html
             broker=RabbitMQCreds.BROKER,
             # http://docs.celeryproject.org/en/latest/userguide/configuration.html#result-backend
             backend=backend,
             )

app.conf.timezone = 'UTC'
app.conf.enable_utc = True
app.autodiscover_tasks()  # Load task modules from all registered Django app configs.
default_exchange = Exchange('default', type='direct', durable=False)

app.conf.update(
    accept_content=['pickle', ],
    task_serializer='pickle',
    result_serializer='pickle',  # https://docs.celeryproject.org/en/master/userguide/calling.html#calling-serializers
    result_extended=True,  # https://docs.celeryproject.org/en/master/userguide/configuration.html#result-extended
    # Do not set! Or logic will not wait of task OK: # task_ignore_result=True,
    task_track_started=True,



    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#result-backend
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#database-url-examples
    # https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#keeping-results
    # 1406, "Data too long for column 'result' at row 1" - it's not so important to keep it in DB
    result_backend=result_backend,
    # result_backend='django-db',
    database_engine_options={'pool_timeout': 300},

    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',

    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-default-queue
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default',
    task_default_exchange_type='direct',

    worker_direct=True,  # http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-direct
    # If enabled (default), any queues specified that aren’t defined in task_queues will be automatically created. See Automatic routing.
    task_create_missing_queues=True,  # Default: Enabled.
    # If set to True, result messages will be persistent. This means the messages won’t be lost after a broker restart.
    # result_persistent=True,  # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-persistent
    # Can be transient (messages not written to disk) or persistent (written to disk).
    task_default_delivery_mode='transient',  # Default: "persistent". https://docs.celeryproject.org/en/master/userguide/configuration.html#task-default-delivery-mode

    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-prefetch-multiplier
    worker_prefetch_multiplier=1,  # NOTE: Do not rely on celery queue no more, use rabbitmq queues instead!

    worker_disable_rate_limits=True,
    worker_concurrency=1,  # https://docs.celeryproject.org/en/master/userguide/configuration.html#worker-concurrency
    worker_lost_wait=20,  # https://docs.celeryproject.org/en/master/userguide/configuration.html#worker-lost-wait
    worker_max_memory_per_child=1024 * 20,  # 20MB
    worker_max_tasks_per_child=100,  # https://docs.celeryproject.org/en/master/userguide/configuration.html#worker-max-tasks-per-child
    worker_proc_alive_timeout=5.0,
    worker_cancel_long_running_tasks_on_connection_loss=True,

    # Useful
    # https://docs.celeryproject.org/en/master/userguide/configuration.html#worker-log-format
    worker_timer_precision=1.0,  # https://docs.celeryproject.org/en/master/userguide/configuration.html#worker-timer-precision
    worker_enable_remote_control=True,  # https://docs.celeryproject.org/en/master/userguide/configuration.html#worker-enable-remote-control
    task_send_sent_event=True,  # https://docs.celeryproject.org/en/master/userguide/configuration.html#task-send-sent-event
    worker_send_task_events=True,  # -E at worker service # http://docs.celeryproject.org/en/latest/userguide/configuration.html#events
    worker_pool_restarts=True,

    # Maybe this should be disabled to allow workers to get ALL tasks in queue.
    task_acks_late=False,  # By Default # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_acks_late
    acks_late=False,  # http://docs.celeryproject.org/en/master/faq.html#faq-acks-late-vs-retry
    task_acks_on_failure_or_timeout=True,  # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-acks-on-failure-or-timeout
    # Setting this to true allows the message to be re-queued instead, so that the task will execute again by the same worker, or another worker.
    task_reject_on_worker_lost=False,  # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-reject-on-worker-lost

    # Broker setup:

    # Automatically try to establish the connection to the AMQP broker on Celery startup if it is unavailable.
    broker_connection_retry_on_startup=True,  # https://docs.celeryq.dev/en/latest/userguide/configuration.html#broker-connection-retry-on-startup
    broker_connection_retry=True,  # Default: Enabled. https://docs.celeryq.dev/en/latest/userguide/configuration.html#broker-connection-retry
    # New in version 5.3.
    # Automatically try to re-establish the connection to the AMQP broker if any invalid response has been returned.
    # RECONNECT RabbitMQ: https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-channel-error-retry
    broker_channel_error_retry=True,  # Default: Disabled.
    # The maximum number of connections that can be open in the connection pool.
    broker_pool_limit=100,  # Default: 10. http://docs.celeryproject.org/en/latest/userguide/configuration.html#broker-pool-limit


    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#broker-connection-timeout
    broker_connection_timeout=4.0,
    broker_connection_max_retries=0,

    broker_heartbeat=10.0,  # https://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_heartbeat
    broker_heartbeat_checkrate=2.0

)

# app.control.cancel_consumer(
#     'default',
#     destination=[
#         "core@layer",
#         "remotes@layer",
#     ])
