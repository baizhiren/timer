# study_main.exe_xx.exe_...
import psutil
import time
from breakTimer.Component import Component
# 根据进程名查找进程
class BlackSheet(Component):
    def __init__(self, list, time_gap=3):
        super().__init__(time_gap=time_gap)
        self.list = list

    def todo(self):
        for proc in psutil.process_iter(['pid', 'name']):
            #print(proc)
            for process_name in self.list:
                if process_name.lower() == proc.info['name'].lower():
                    pid = proc.info['pid']
                    p = psutil.Process(pid)
                    print(f'黑名单{proc.info["name"]}')
                    p.terminate()



if __name__ == '__main__':
    blackSheet = BlackSheet(['msedge.exe', 'steam.exe'])
    blackSheet.start()
    time.sleep(100000)