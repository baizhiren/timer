import time

from breakTimer.Component import Component


class A(Component):
    def __init__(self, time_gap=3):
        super().__init__(time_gap=time_gap, name='禁用键盘')

    def todo(self):
        print(1 / 0)

# 不可以
# if __name__ == '__main__':
#     m = A()
#     m.start()
#     time.sleep(10000)
