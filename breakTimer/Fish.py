import threading
import time

from breakTimer.Component import Component

# 重写todo方法
class Fish(Component):
    def __init__(self, **kwargs):
        super().__init__(name=kwargs.get('fish_name', 'fish'))
        self.happen = kwargs["semaphore"]

    def start_swim(self) -> bool:
        print('fish is flying...')
        time.sleep(3)
        return True

    def done(self):
        self.happen.release()

    def todo(self):
        res = self.start_swim()
        if res:
            self.done()