import json
import multiprocessing
import time
import tkinter as tk
from functools import partial
from threading import Thread, Timer
from tkinter import ttk
from tkinter.messagebox import showinfo
import pyautogui as ui

from breakTimer.SystemMusic import SystemMusic

ui.FAILSAFE = False


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
    stageInfoVar = tk.StringVar()
    music = SystemMusic()

    smallTime = 5
    bigTime = 20
    studyTime = 45
    smallNum = 1

    path = 'config.json'
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)  # 加载我们的数据
            smallTime = data.get('smallTime', 5)
            bigTime = data.get('bigTime', 20)
            studyTime = data.get('studyTime', 45)
            smallNum = data.get('smallNum', 1)
    except:
        pass

    small.set(smallTime)
    big.set(bigTime)
    study.set(studyTime)
    smallNumVar.set(smallNum)

    update = 0
    end = True


    def stage(name, t, before_update):
        print(f"hello, thfis is stage {name}")
        global end
        # mouse_end = False
        # def cover():
        #     while not end:
        #         root.attributes('-fullscreen', True)
        #         root.attributes('-fullscreen', False)
        #         root.geometry("300x300")
        #
        # def cover2():
        #     while not mouse_end:
        #         ui.click(200, 200, button='MIDDLE')
        #
        # def cover3():
        #     while not end:
        #         ui.hotkey('ctrl', 'alt')

        if before_update != update:
            return
        t = t * 60
        fullStage = '学习阶段'
        if name == fullStage:
            root.attributes('-topmost', 1)
            root.attributes('-fullscreen', True)
            root.deiconify()
            end = False
            login_button.configure(state='disable')
            # email_entry.state = "readonly"
            # password_entry.state = "readonly"
        global stageInfo
        for i in range(t):
            stageInfo = f'当前阶段:{name}  剩余时间:{t // 60}分: {t % 60}秒'
            stageInfoVar.set(stageInfo)
            stageInfoVar.set(stageInfo)
            time.sleep(1)
            t = t - 1
            # if t <= 20:
            #     mouse_end = True
            if before_update != update:
                break


        if name == fullStage:
            root.attributes('-fullscreen', False)
            root.geometry("300x300")
            root.attributes('-topmost', 0)
            end = True
            login_button.configure(state='enable')
        if before_update == update:
            music.ring(n=2)


    def run():
        st = 0
        for i in range(int(smallNum)):
            t1 = Timer(st * 60, partial(stage, name='学习阶段', t=studyTime, before_update=update))
            #t1.setDaemon(True)
            t1.start()
            st += int(studyTime)
            t2 = Timer(st * 60, partial(stage, name='休息阶段', t=smallTime, before_update=update))
            t2.start()
            #t2.setDaemon(True)
            st += int(smallTime)

        Timer(st * 60, partial(stage, name='学习阶段', t=studyTime, before_update=update)).start()
        st += int(studyTime)
        Timer(st * 60, partial(stage, name='休息阶段', t=bigTime, before_update=update)).start()
        st += int(bigTime)

    # daemon=True
    Thread(target=run, daemon=True).start()
    #old.start()


    def close():
        while not end:
            pass
        root.quit()
        global update
        update = update + 1

    def quit_me():
        Timer(0, close).start()
        data = {}
        with open(path, "w", encoding="utf-8") as f:
            data["smallTime"] = smallTime
            data["bigTime"] = bigTime
            data["studyTime"] = studyTime
            data["smallNum"] = smallNum
            json.dump(data, f, indent=3, ensure_ascii=False)


    root.protocol("WM_DELETE_WINDOW", quit_me)


    def login_clicked():
        """ callback when the login button clicked
        """
        global smallTime, bigTime, studyTime, smallNum
        msg = ''
        if not small.get().isdigit():
            msg = '小休息时间必须是数字！'
        if not big.get().isdigit():
            msg = '大休息时间必须是数字！'
        elif not study.get().isdigit():
            msg = '学习时间必须是数字！'
        elif not smallNumVar.get().isdigit():
            msg = '小学次数必须是数字！'
        else:
            msg = f'修改成功'

            global update
            update = update + 1
            smallTime = int(small.get())
            bigTime = int(big.get())
            studyTime = int(study.get())
            smallNum = int(smallNumVar.get())

            #global old
            #old.daemon = True
            Thread(target=run, daemon=True).start()
            #old.start()

            # global olds
            # if olds is not None:
            #     olds.terminate()
            # olds = Process(target=run)
            # olds.start()

        showinfo(
            title='改变成功',
            message=msg
        )


    # Sign in frame
    signin = ttk.Frame(root)
    signin.pack(padx=10, pady=10, fill='x', expand=True)

    email_label = ttk.Label(signin, textvariable=stageInfoVar)
    email_label.pack(fill='x', expand=True)

    email_label = ttk.Label(signin, text="小休息时间")
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
