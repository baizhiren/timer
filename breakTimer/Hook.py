import threading
import time

from breakTimer.Fish import Fish
from breakTimer.Plug import Plug


class Hook(Plug):
    #  Hook.__init__(self, cls, path)
    def __init__(self, fish_cls:type[Fish], count:int=0, name='hook', **kwargs):
        super().__init__(name=name)
        self.semaphore = threading.Semaphore(count)
        kwargs["semaphore"] = self.semaphore
        self.fish = self.create_object(fish_cls, **kwargs)
        self.fish.start()

    def start_fish(self):
        print('hook get a fish!')

    def todo(self):
        self.semaphore.acquire(1)
        self.start_fish()

    @staticmethod
    def create_object(cls, *args, **kwargs):
        return cls(*args, **kwargs)

# if __name__ == '__main__':
#     h = Hook(Fish)
#     h.start()
#     time.sleep(50)






