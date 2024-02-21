import traceback
from typing import Dict
from tools.timeParser import *

custom_exception = type("para Error", (Exception,), {"__str__": lambda self: "用户参数错误"})


def check(awake: Dict[str, str]):
    try:
        if awake["mode"] == 'day':
            interval = awake["interval"]
            st, ed = parseInterval(interval)
            return check_interval(st, ed)
        elif awake["mode"] == 'week':
            value = awake["value"]
            interval = awake["interval"]
            return checkWeek(interval, value)
        elif awake["mode"] == 'period':
            interval = awake["interval"]
            st, ed = parsePeriod(interval)
            return checkPeriod(st, ed)

        elif awake["mode"] == 'always':
            return True
        else:
            print('未知参数', awake["mode"])
            return False

    except Exception as e:
        print('异常', e)
        print(traceback.print_exc())
        raise custom_exception

def check_expire(awake: Dict[str, str]):
    try:
        if awake["mode"] == 'period':
            interval = awake["interval"]
            st, ed = parsePeriod(interval)
            return check_period_expire(ed)
        return False
    except Exception as e:
        print('异常', e)
        print(traceback.print_exc())
        raise custom_exception


