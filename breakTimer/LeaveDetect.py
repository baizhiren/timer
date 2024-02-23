#线程1： 倒计时x分钟
#线程2，不断的检测键盘
import time
from threading import Thread
from breakTimer.exceptions import my_exception

import keyboard


class LeaveDetect:
    def __init__(self, end_function, count_down=10, detect_keyboard_time=5):
        if detect_keyboard_time > count_down:
            raise my_exception('键盘检测时间不能大于倒计时')
        self.count_down = count_down
        self.init_count_down = count_down
        self.detect_keyboard_time = detect_keyboard_time
        self.end_function = end_function
        self.end = False
        pass


    def start_count_donw(self):
        while not self.end:
            self.count_down -= 1
            if self.count_down < 0:
                break
            time.sleep(1)
        print('倒计时结束，boom！')
        if not self.end:
            self.end_function()

    def detect_keyborad(self):
        while not self.end:
            keyboard.read_key()
            self.count_down = self.init_count_down
            # print('重置倒计时')
            time.sleep(self.detect_keyboard_time)

    def start(self):
       Thread(target=self.start_count_donw).start()
       Thread(target=self.detect_keyborad).start()

    def stop(self):
        self.end = True

debug = True
if debug:
    if __name__ == '__main__':
        def end_function():
            print('这是未来啊，要抓住！')

        ld = LeaveDetect(end_function)
        ld.start()
        time.sleep(10000)













