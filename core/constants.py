"""
Celery tasks and related cont variables.
"""
import core.setup_logic

DAY_LIMIT = 172800

HOURS_1 = 3600
HOURS_2 = 7200
HOURS_3 = HOURS_1 * 3
HOURS_4 = HOURS_2 * 2
HOURS_5 = HOURS_4 + HOURS_1

MIN_90 = 5400
MIN_40 = 2400
MIN_20 = 1200
MIN_10 = 600
MIN_5 = 300

MIN_1 = 60

SEC_10 = 10
SEC_1 = 1

# Jan 19 (Wednesday) 07:53
TASK_F = "%b %d (%a) %H:%M:%S"

"""
Common variables used in system
"""

COMMON_F = '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
COMMON_SLASHED = '%m/%d/%Y %H:%M:%S',  # '10/25/2006 14:30:59'
COMMON_SLASHED_y = '%m/%d/%y %H:%M:%S',  # '10/25/06 14:30:59'


def is_dev():
    """
    Check for local ENV exclusively
    """
    if core.setup_logic.ENV == 0:
        return True
    return False


def is_test():
    """
    Understand the ENV we are working on.
    If this is a local ENV or Lobster Dev env.
    """
    if core.setup_logic.ENV == 0:
        return True
    elif core.setup_logic.ENV == 1:
        return True
    return False
