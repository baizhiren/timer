import time
from threading import Thread



# 根据进程名查找进程
class Component:

    def __init__(self, time_gap=5, name=' '):
        self.time_gap = time_gap
        self.is_end = False
        self.name = name

    def todo(self):
        pass

    def start(self):
        Thread(target=self.__start__, daemon=True).start()

    def __start__(self):
        # try:
        self.todo()
        # except Exception as e:
        #     print(f'定时任务{self.name}错误', e)
        time.sleep(self.time_gap)
        if not self.is_end:
            self.__start__()

    def stop(self):
        self.is_end = True
