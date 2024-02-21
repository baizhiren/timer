import time
import traceback
from threading import Thread

# 根据进程名查找进程
class Plug:
    def __init__(self, name=' '):
        self.name = name

    def todo(self):
        pass

    def start(self):
        Thread(target=self.__start__, daemon=True).start()

    def __start__(self):
        try:
            self.todo()
        except Exception as e:
            print(f'任务{self.name}错误', e)
            print(traceback.print_exc())

    def stop(self):
        pass
