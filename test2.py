# -*- coding:utf-8 -*-
import threading
import time
import winsound

MinuteToSecond = 60 * 1000
cancel_tmr = False
duration = 1000  # 持续时间/ms
frequency = 500  # 频率/Hz

def heart_beat():
    # 打印当前时间
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    if not cancel_tmr:
        #winsound.Beep(frequency, duration)
        # 每隔3秒执行一次
        threading.Timer(3, heart_beat).start()



if __name__ == '__main__':
    heart_beat()
