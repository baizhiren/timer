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
        Thread(target=self.__start__, daemon=True, name=self.name).start()

    def __start__(self):
        try:
            self.todo()
        except Exception as e:
            self.error()
            print(f'任务{self.name}错误', e)
            print(traceback.print_exc())

    def stop(self):
        pass

    def error(self):
        pass

# if __name__ =='__main__':
#     p = Plug()
#     p.start()
#     from tools.printThread import *
#
#     show_all_threads()

