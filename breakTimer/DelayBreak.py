import time

from breakTimer.Plug import Plug
import keyboard



#1.休息模式的时候，如果读到三次键盘敲击，就会就会进入一个新的学习阶段

class DelayBreak(Plug):
    def __init__(self,  func, count=3):
        super().__init__(name='禁用键盘')
        self.func = func
        self.count = count
        self.is_end = False
        self.enter_pressed = False

    def on_enter_press(self, event):
        if event.name == 'enter':
            print('press enter')
            self.count -= 1
            if self.count <= 0:
                self.enter_pressed = True

    def todo(self):
        keyboard.on_press(self.on_enter_press)  # 注册按键回调函数

        while not self.is_end and not self.enter_pressed:
            time.sleep(5)  # 睡眠一小段时间，避免 CPU 资源的浪费

        keyboard.unhook_all()  # 关闭键盘监听

        if not self.is_end:
            self.func()

    def stop(self):
        self.is_end = True




# 不可以
# if __name__ == '__main__':
#     def x():
#         print('lalaland')
#     m = DelayBreak(x)
#     m.start()
#     time.sleep(3)
#     print('unhook')
#     m.stop()
#     time.sleep(1)
#     m.start()
#     time.sleep(1)
#     m.stop()
#     print('第二次关闭')
#
#     from tools.printThread import *
#
#     show_all_threads()
#     time.sleep(1000)
#

