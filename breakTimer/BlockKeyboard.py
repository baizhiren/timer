import time

from breakTimer.Plug import Plug
import keyboard


class BlockKeyBoard(Plug):
    def __init__(self):
        super().__init__(name='禁用键盘')
        self.enter_count = 0
        self.threshold = 99

    def on_press(self, event):
        global enter_count
        if event.event_type == keyboard.KEY_DOWN and event.name == 'enter':
            self.enter_count += 1
            if self.enter_count % 5 == 0:
                print(f'按了{self.enter_count}次')
            if self.enter_count == self.threshold:
                keyboard.unhook_all()
                keyboard.on_press(self.on_press)
                print("用户按下了规定次数的Enter 键，解除锁定")
            elif self.enter_count == self.threshold + 1:
                print('很不幸，重新进入锁定模式')
                self.enter_count = 0
                self.block_keys()

                # 执行你的逻辑

    def todo(self):
        self.block_keys()
        keyboard.on_press(self.on_press)

    def block_keys(self):
        keyboard.block_key('a')  # 禁用按键 'a'
        keyboard.block_key('b')  # 禁用按键 'b'
        for letter in range(ord('a'), ord('z') + 1):
            keyboard.block_key(chr(letter))
        for i in range(10):
            keyboard.block_key(i)
        keyboard.block_key('ctrl')
        keyboard.block_key('alt')
        keyboard.block_key('esc')
        keyboard.block_key('shift')
        keyboard.block_key('windows')

    def stop(self):
        keyboard.unhook_all()


# 不可以
# if __name__ == '__main__':
#     m = BlockKeyBoard()
#     m.start()
#     time.sleep(10)
#     m.stop()
#     time.sleep(1)
#     from tools.printThread import *
#
#     show_all_threads()
#
