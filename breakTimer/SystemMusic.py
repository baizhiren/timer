import threading
import time
import winsound
from playsound import playsound

class SystemMusic:
    duration = 1000  # 持续时间/ms
    frequency = 500  # 频率/Hz
    cancel_tmr = False
    time_gap = 3
    song = ['shine.wav']

    def __init__(self, **kw):
        for k, v in kw:
            self.k = v

    def ring(self, time_gap=3, n=5, id=0):
        if id == -1:
            self.time_gap = time_gap
            self.heart_beat()
            time.sleep(time_gap * n)
            self.cancel_tmr = True
            time.sleep(5)
            self.cancel_tmr = False
        else:
            for i in range(n):
                playsound(self.song[id])

    def beep(self):
        winsound.Beep(self.frequency, self.duration)

    def heart_beat(self):
        # 打印当前时间
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        if not self.cancel_tmr:
            threading.Timer(0, self.beep).start()
            # 每隔3秒执行一次
            threading.Timer(self.time_gap, self.heart_beat).start()