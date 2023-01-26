import time
import datetime
a = (1, 2, 3)
b = (1, 2, 3)
print(a == b)


now = time.localtime(time.time())
print(now)
date = datetime.datetime(now[0], now[1], now[2], now[3], now[4], now[5])
date2 = datetime.datetime(now[0], now[1], now[2], now[3], now[5], now[5])
print(date == date2)

print(date + datetime.timedelta(hours=1))