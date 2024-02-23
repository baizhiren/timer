from datetime import datetime
from typing import List


def parseInterval(interval:str):
    start_time_str, end_time_str = interval.split('-')
    # 将字符串解析为时间
    start_time = datetime.strptime(start_time_str, '%H:%M')
    end_time = datetime.strptime(end_time_str, '%H:%M')
    return start_time, end_time

# 判断当前时间是否位于给定的区间内
def check_interval(start_time:datetime, end_time: datetime):
    now = datetime.now()
    now = now.replace(year=start_time.year, month=start_time.month, day=start_time.day)
    res = start_time <= now <= end_time
    return res


def parsePeriod(interval:str):
    start_str, end_str = interval.split('-')

    # 解析字符串为 datetime 对象
    start_time = datetime.strptime(start_str, '%Y.%m.%d %H:%M')
    end_time = datetime.strptime(end_str, '%Y.%m.%d %H:%M')

    # print(start_time)  # 输出：2024-02-20 08:30:00
    # print(end_time)  # 输出：2024-02-26 08:30:00
    return start_time, end_time

def checkPeriod(start_time:datetime, end_time: datetime):
    now = datetime.now()
    return start_time <= now <= end_time

def check_period_expire(end_time:datetime):

    now = datetime.now()
    return end_time <= now


def checkWeek(interval:str, value:List[int]):
    start_time, end_time = parseInterval(interval)
    now = datetime.now()
    week = now.weekday()
    return week + 1 in value and check_interval(start_time, end_time)

if __name__ == '__main__':
    st, ed = parsePeriod('2024.2.20 8:30-2024.2.26 8:30')
    print(st, ed)
