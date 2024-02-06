# study_main.exe_xx.exe_...
import psutil
import time
from breakTimer.Component import Component
# 根据进程名查找进程
class BlackSheet(Component):
    def __init__(self, list, time_gap=3):
        super().__init__(time_gap=time_gap, name='黑名单')
        self.list = list

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