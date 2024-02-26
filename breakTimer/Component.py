import time
import traceback
from threading import Thread



# 根据进程名查找进程
from typing import Dict
from breakTimer.Awake import check
from breakTimer.Plug import Plug


class Component(Plug):
    def __init__(self, time_gap=5, name='组件', todo='', awake:Dict[str, str]=None, retry=False):
        self.time_gap = time_gap
        self.is_end = False
        self.name = name
        self.awake = awake
        self.retry = retry
        if todo != '':
            self.todo = todo

    def __start__(self):
        while not self.is_end:
            try:
                if self.awake != None:
                    if not check(self.awake):
                        continue
                self.todo()
            except Exception as e:
                self.error()
                print(f'任务{self.name}错误', e)
                print(traceback.print_exc())
                if not self.retry:
                    break
            time.sleep(self.time_gap)

    def stop(self):
        self.is_end = True

