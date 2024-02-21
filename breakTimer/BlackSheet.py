# study_main.exe_xx.exe_...
from typing import *

import psutil
import time

from breakTimer.Awake import check
from breakTimer.Component import Component
# 根据进程名查找进程
from exception.exceptions import custom_exception
class BlackSheet(Component):
    def __init__(self, black_lists:List[Dict[str, str]], time_gap=3, click=False):
        super().__init__(time_gap=time_gap, name='黑名单')
        self.black_lists = black_lists
        self.click = click
        self.list = []
        try:
            for black_list in self.black_lists:
                enable = black_list["enable"]
                if not enable:
                    continue
                list = black_list["list"]
                name = black_list["name"]
                print(f'开启黑名单{name}')

                time = black_list["time"]

                if time == "click":
                    if self.click:
                        self.list += list
                elif check(time):
                    self.list += list
        except:
            raise custom_exception

    def todo(self):
        for proc in psutil.process_iter(['pid', 'name']):
            #print(proc)
            for process_name in self.list:
                if process_name.lower() == proc.info['name'].lower():
                    print(f'黑名单{proc.info["name"]}')
                    try:
                        pid = proc.info['pid']
                        p = psutil.Process(pid)
                        p.terminate()
                    except Exception as e:
                        print(e)
                        print('关闭', proc, '错误')


# 不可以
# if __name__ == '__main__':
#     blackSheet = BlackSheet(['msedge.exe', 'steam.exe'])
#     blackSheet.start()
#     time.sleep(100000)