import argparse
import os
import socket
import subprocess
import sys
from queue import Queue
from threading import Thread
from time import time


from core.security import CeleryCreds, HostnamesSupported

hostname = socket.gethostname()


ENV = 0
print("Setup celery environment.")
# LOCAL DEV
if hostname == HostnamesSupported.DEV_HOSTNAME:
    ENV = 0
    CELERY_BIN = "/home/user/projects/my_vps/venv/bin/celery"
    CWD = "/mnt/d/Projects/PycharmProjects/my_vps/"
    CELERYD_PID_FILE = "/home/user/{PID}.pid"
    CELERY_LOG_PATH = '/mnt/d/Projects/PycharmProjects/my_vps/'
    workers = CeleryCreds.WSL_WORKERS
    CELERYD_LOG_LEVEL = "INFO"
    print(f"Celery ENV LOCAL: {hostname} ENV={ENV} CELERY_BIN:{CELERY_BIN} workers: {workers}")
# LIVE
elif hostname == HostnamesSupported.LIVE_HOSTNAME:
    ENV = 1
    CELERY_BIN = "/var/www/my_vps/venv/bin/celery"
    CWD = "/var/www/my_vps/"
    CELERYD_PID_FILE = "/opt/celery/{PID}.pid"
    CELERY_LOG_PATH = '/var/log/my_vps/'
    workers = CeleryCreds.WORKERS
    CELERYD_LOG_LEVEL = "INFO"
    print(f"Celery ENV Live: {hostname} ENV={ENV} CELERY_BIN:{CELERY_BIN} workers: {workers}")
else:
    print(f"ERROR: Celery ENV UNSUPPORTED: {hostname} ENV={ENV}")
    sys.exit(f"ERROR: Celery ENV UNSUPPORTED: {hostname} ENV={ENV}")


CELERY_APP = "core.core_celery:app"
CELERYD_LOG_FILE = "{PATH}/{LOG}.log"
CELERYD_OPTS = "--concurrency=1 -E"
CELERYD_NODES = workers


commands_list_start = "python3 {CELERY_BIN} multi start " \
                      "{celery_node} -A {CELERY_APP} " \
                      "--pidfile={CELERYD_PID_FILE} " \
                      "--logfile={CELERYD_LOG_FILE} " \
                      "--loglevel={CELERYD_LOG_LEVEL} --concurrency=1 -E"

commands_list_stop = "python3 {CELERY_BIN} multi kill " \
                     "{celery_node} -A {CELERY_APP} " \
                     "--pidfile={CELERYD_PID_FILE} " \
                     "--logfile={CELERYD_LOG_FILE} " \
                     "--loglevel={CELERYD_LOG_LEVEL}"

commands_list_restart = "python3 {CELERY_BIN} multi restart " \
                        "{celery_node} -A {CELERY_APP} " \
                        "--pidfile={CELERYD_PID_FILE}"

commands_list_kill = "pkill -9 -f 'core.core_celery:app worker " \
                     "--pidfile={CELERYD_PID_FILE}'"


def th_run(args):
    # print(args)
    mode = args.mode
    worker_list = args.worker
    print(f'Run celery commands: {mode}, {worker_list}')

    stat = dict(
        start=commands_list_start,
        stop=commands_list_stop,
        restart=commands_list_restart,
        kill=commands_list_kill,
    )

    ts = time()
    thread_list = []
    th_out = []
    test_q = Queue()

    if worker_list:
        workers = [worker + "@layer" for worker in worker_list]
    else:
        workers = CELERYD_NODES

    for celery_node in workers:
        cmd_draft = stat[mode]
        cmd = cmd_draft.format(
            CELERY_BIN=CELERY_BIN,
            celery_node=celery_node,
            CELERY_APP=CELERY_APP,
            CELERYD_PID_FILE=CELERYD_PID_FILE.format(PID=celery_node),
            CELERYD_LOG_FILE=CELERYD_LOG_FILE.format(PATH=CELERY_LOG_PATH, LOG=celery_node),
            CELERYD_LOG_LEVEL=CELERYD_LOG_LEVEL,
            CELERYD_OPTS=CELERYD_OPTS,
        )
        print(f"Run: {cmd}")
        args_d = dict(cmd=cmd, test_q=test_q)
        th_name = f"Run CMD: {cmd}"
        try:
            test_thread = Thread(target=worker_restart, name=th_name, kwargs=args_d)
            test_thread.start()
            thread_list.append(test_thread)
        except Exception as e:
            msg = "Thread test fail with error: {}".format(e)
            print(msg)
            return msg
    # Execute threads:
    for th in thread_list:
        th.join()
        th_out.append(test_q.get())
    print(f'All run Took {time() - ts} Out {th_out}')


def worker_restart(**args_d):
    cmd = args_d.get('cmd')
    test_q = args_d.get('test_q')
    cwd = CWD
    my_env = os.environ.copy()
    run_results = []
    try:
        run_cmd = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=cwd,
                                   env=my_env,
                                   shell=True,
                                   )
        # run_cmd.wait()
        stdout, stderr = run_cmd.communicate()
        stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
        run_results.append({'stdout': stdout, 'stderr': stderr})
        test_q.put(run_results)
    except Exception as e:
        msg = f"<=run_subprocess=> Error during operation for: {cmd} {e}"
        test_q.put(msg)
        print(msg)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-m', '--mode', choices=['start', 'stop', 'restart', 'kill'], required=True)
parser.add_argument('-w', '--worker', action='append')
th_run(parser.parse_args())


"""
Usage:
python celery_restart.py --mode=start
python celery_restart.py --mode=kill --worker=core; python celery_restart.py --mode=start --worker=core
python celery_restart.py --mode=kill
python celery_restart.py --mode=restart
python celery_restart.py --mode=restart --worker=w_parsing


python3 /var/www/my_vps/venv/bin/celery multi start core@layer -A core.core_celery:app --pidfile=/opt/celery/core@layer.pid --logfile=/var/log/my_vps/core@layer.log --loglevel=INFO --concurrency=1 -E
python3 /var/www/my_vps/venv/bin/celery -A core.core_celery:app worker --loglevel=INFO

celery --app=proj worker -l INFO $ celery -A proj worker -l INFO -Q hipri,lopri
celery -A proj worker --concurrency=4 $ celery -A proj worker --concurrency=1000 -P eventlet 
celery worker --autoscale=10,0

python3 /var/www/my_vps/venv/bin/celery --app=core.core_celery:app worker core --concurrency=5 --detach

celery -A core.core_celery:app worker --loglevel=INFO


# For WIN
celery -A core.core_celery:app beat --loglevel=INFO
# Older:
python celery_restart.py --mode=kill --worker=beat; python celery_restart.py --mode=beat --worker=beat
"""

"""
celery multi start remotes@layer -A core.core_celery:app --pidfile=remotes@layer.pid --logfile=remotes@layer.log --loglevel=INFO --concurrency=1 -E

Windows workaround:
# Only working:
celery -A core.core_celery:app worker --logfile=remotes@layer.log --loglevel=INFO --concurrency=1 -E -P eventlet
"""


