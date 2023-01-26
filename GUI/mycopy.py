import multiprocessing
import tkinter as tk
from threading import Thread
from tkinter import ttk
from tkinter.messagebox import showinfo
from multiprocessing import Process


from breakTimer.BreakTimer import BreakTimer

if __name__ == '__main__':
    multiprocessing.freeze_support()
    # root window
    root = tk.Tk()
    root.geometry("300x300")
    root.resizable(False, False)
    root.title('休息定时器')

    # store email address and password
    small = tk.StringVar()
    big = tk.StringVar()
    study = tk.StringVar()
    smallNumVar = tk.StringVar()


    smallTime = 5
    bigTime = 30
    studyTime = 45
    smallNum = 1

    small.set(smallTime)
    big.set(bigTime)
    study.set(studyTime)
    smallNumVar.set(smallNum)

    breakTimer = BreakTimer(smallTime, bigTime, studyTime, smallNum)
    olds = Process(target=breakTimer.start)
    olds.start()


    def login_clicked():
        """ callback when the login button clicked
        """
        smallTime = small.get()
        bigTime = big.get()
        studyTime = study.get()
        smallNum = smallNumVar.get()
        msg = ''
        if not smallTime.isdigit():
            msg = '小休息时间必须是数字！'
        if not bigTime.isdigit():
            msg = '大休息时间必须是数字！'
        elif not studyTime.isdigit():
            msg = '学习时间必须是数字！'
        elif not smallNum.isdigit():
            msg = '小学次数必须是数字！'
        else:
            msg = f'小休时间: {smallTime} and 大休时间: {bigTime}'
            global olds
            if olds is not None:
                olds.terminate()
            breakTimer = BreakTimer(int(smallTime), int(bigTime), int(studyTime), int(smallNum))
            olds = Process(target=breakTimer.start)
            olds.start()

        showinfo(
            title='改变成功',
            message=msg
        )


    # Sign in frame
    signin = ttk.Frame(root)
    signin.pack(padx=10, pady=10, fill='x', expand=True)

    email_label = ttk.Label(signin, text="小休时间")
    email_label.pack(fill='x', expand=True)

    email_entry = ttk.Entry(signin, textvariable=small)
    email_entry.pack(fill='x', expand=True)
    email_entry.focus()


    password_label = ttk.Label(signin, text="大休时间:")
    password_label.pack(fill='x', expand=True)

    password_entry = ttk.Entry(signin, textvariable=big)
    password_entry.pack(fill='x', expand=True)


    email_label = ttk.Label(signin, text="学习时间")
    email_label.pack(fill='x', expand=True)

    email_entry = ttk.Entry(signin, textvariable=study)
    email_entry.pack(fill='x', expand=True)
    email_entry.focus()

    email_label = ttk.Label(signin, text="小学次数")
    email_label.pack(fill='x', expand=True)

    email_entry = ttk.Entry(signin, textvariable=smallNumVar)
    email_entry.pack(fill='x', expand=True)
    email_entry.focus()



    # login button
    login_button = ttk.Button(signin, text="确定", command=login_clicked)
    login_button.pack(fill='x', expand=True, pady=10)


    root.mainloop()