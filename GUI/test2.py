import tkinter as tk
from threading import Timer, Thread


def hello():
    print("hello,world")

Thread(Timer(0, hello)).start()



