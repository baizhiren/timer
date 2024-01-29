import time
from threading import Thread



# 根据进程名查找进程
class Component:

    def __init__(self, time_gap=5):
        self.time_gap = time_gap
        self.is_end = False

    def todo(self):
        pass

    def start(self):
        Thread(target=self.__start__, daemon=True).start()

    def __start__(self):
        self.todo()
        time.sleep(self.time_gap)
        if not self.is_end:
            self.__start__()

    def stop(self):
        self.is_end = True
