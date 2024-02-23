import sys


def is_debug():
    if getattr(sys, 'frozen', False):
        # 在可执行文件中运行的逻辑
        print("在可执行文件中运行")
        return  False
    return True