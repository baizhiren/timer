import hashlib
import json
import threading
import time

from breakTimer.Component import Component
from breakTimer.Fish import Fish
from breakTimer.Hook import Hook

import os
import datetime



# 接收者
class FileChecker(Fish):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = kwargs['path']
        self.last_modify = -1
        self.last_hash = -1
        self.count = 0 # 官方修改的次数

    def start_swim(self):
        hash = self.calculate_file_hash(self.path)
        if self.last_hash == -1:
            self.last_hash = hash
            return False
        elif self.last_hash != hash:
            while True:
                time.sleep(5)
                next_hash = self.calculate_file_hash(self.path)
                if hash == next_hash:
                    self.last_hash = hash
                    break
                hash = next_hash
            with open(self.path, 'r', encoding='utf-8') as file:
                content = file.read()
            print('检测到文件修改: ', content)
            return True

    def add(self):
        self.count += 1

    @staticmethod
    def calculate_file_hash(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            file_hash = hashlib.md5(content).hexdigest()
        return file_hash


# 不可以
# if __name__ == '__main__':
#     class JsonWriter(Component, Hook):
#         def __init__(self, cls, **kwargs):
#             Hook.__init__(self, cls, **kwargs)
#             super().__init__(name='jsonWriter')
#
#         def start_fish(self):
#             print('文件被修改！')
#
#
#     jsonWriter = JsonWriter(FileChecker, **{'path':'../test/temp.txt', 'fish_name':'file checker'})
#     print('jsonWriter name:', jsonWriter.name)
#     print('fish name', jsonWriter.fish.name)
#     jsonWriter.start()
#     time.sleep(100000)
#     with open('', 'r', encoding='utf-8') as file:
#         file = json.load(file)
#     print(file)




    # def start_swim(self):
    #     # 获取文件的上次修改时间戳
    #     timestamp = os.path.getmtime(self.path)
    #
    #     # 将时间戳转换为可读的日期时间格式
    #     modified_time = datetime.datetime.fromtimestamp(timestamp)
    #     modified_time = modified_time.replace(microsecond=0)
    #
    #     # 打印文件的上次修改时间
    #     print("File last modified time:", modified_time)
    #
    #     if self.last_modify == -1:
    #         self.last_modify = modified_time
    #         return False
    #     elif self.last_modify != modified_time:
    #         self.last_modify = modified_time
    #         print('检测到文件修改！')
    #         if self.count > 0:
    #             self.count -=1
    #             return False
    #         return True
    #     return False