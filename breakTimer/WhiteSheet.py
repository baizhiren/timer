# study_main.exe_xx.exe_...
from typing import *

import psutil
import time

from breakTimer.Plug import Plug
from breakTimer.Awake import *
# 根据进程名查找进程
from exception.exceptions import custom_exception
class WhiteSheet(Plug):
    def __init__(self, white_lists:List[Dict[str, str]]):
        super().__init__(name="白名单")
        self.white_lists = white_lists
        print(f'白名单{self.white_lists}')

    def get_new_white_sheet(self):
        res = []
        flag = False
        for time in self.white_lists:
            if not check_expire(time):
                res += time
            else:
                flag = True
        return res, flag

    def todo(self):
        for time in self.white_lists:
            if check(time):
                return True
        return False



# 不可以
# if __name__ == '__main__':
#     blackSheet = BlackSheet(['msedge.exe', 'steam.exe'])
#     blackSheet.start()
#     time.sleep(100000)