from threading import Timer
from tkinter import *

root = Tk()


def run():
    print(f'x: {root.winfo_rootx()} y: {root.winfo_rooty()}')
    print(f'{root.winfo_x()} y: {root.winfo_y()}')

for i in range(100):
   Timer(i * 3, run).start()

root.mainloop()