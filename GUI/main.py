import json
import time
import tkinter as tk
import datetime
from functools import partial
from threading import Thread, Timer
from tkinter import ttk
from tkinter.messagebox import showinfo
import pyautogui as ui

from breakTimer.SystemMusic import SystemMusic

ui.FAILSAFE = False


if __name__ == '__main__':
    # multiprocessing.freeze_support()
    root = tk.Tk()
    #size = "8000x3000+-4000+0"
    #size = "400x400+500+500"
    root.resizable(False, False)
    root.title('休息定时器3.1')

    small = tk.StringVar()
    big = tk.StringVar()
    study = tk.StringVar()
    smallNumVar = tk.StringVar()
    stageInfoVar = tk.StringVar()
    pauseVar = tk.StringVar()

    music = SystemMusic()
    isLoop = tk.IntVar()
    cnt_round = tk.StringVar()
    cnt_round.set('肝数:0')
    pauseVar.set('暂停')

    smallTime = 6
    bigTime = 12
    studyTime = 40
    smallNum = 3
    is_loop = 0
    liver = "22:30"
    liver_to = "6:00"
    force = 1
    width = "450"
    length = "450"
    is_music = 0


    path = 'config.json'
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)  # 加载我们的数据
            smallTime = data.get('smallTime', smallTime)
            bigTime = data.get('bigTime', bigTime)
            studyTime = data.get('studyTime', studyTime)
            smallNum = data.get('smallNum', smallNum)
            is_loop = data.get('isLoop', isLoop)
            liver = data.get('liver', liver)
            liver_to = data.get('liver_to', liver)
            force = data.get('force', force)
            width = data.get('width', width)
            length = data.get('length', length)
            is_music = data.get('is_music', is_music)
    except:
        pass

    small.set(smallTime)
    big.set(bigTime)
    study.set(studyTime)
    smallNumVar.set(smallNum)
    isLoop.set(is_loop)
    size = width + "x" + length + "+500+500"
    root.geometry(size)


    update = 0
    end = True
    lastEnd = True
    pause = False

    # 1 1 2 1 2 1
    def stage(name, t, before_update):
        print(f"hello, this is stage {name}")
        global end, lastEnd, update

        if before_update != update and name != '养肝阶段':
            return
        if name == '养肝阶段':
            update = update + 1

        while not lastEnd:
            time.sleep(1)
        lastEnd = False
        t = t * 60
        fullStage = ['休息阶段', '养肝阶段']
        if name in fullStage:
            root.attributes('-topmost', 1)
            if force:
                root.attributes('-fullscreen', True)
            root.deiconify()
            end = False
            login_button.configure(state='disable')
            break_now_button.configure(state='disable')

        global stageInfo
        #t = 3
        for i in range(t):
            stageInfo = f'当前阶段:{name}  剩余时间:  {t // 60}分 : {t % 60}秒'
            stageInfoVar.set(stageInfo)
            stageInfoVar.set(stageInfo)
            time.sleep(1)
            t = t - 1
            while pause:
                time.sleep(1)
            if before_update != update and name != '养肝阶段':
                break
        stageInfoVar.set(f'当前阶段:{name}  剩余时间: 0分 : 0秒')
        if name in fullStage:
            root.attributes('-fullscreen', False)
            root.geometry(size)
            root.attributes('-topmost', 0)
            end = True
            login_button.configure(state='enable')
            break_now_button.configure(state='enable')
        lastEnd = True
        if before_update == update:
            if is_music:
                music.ring(n=2)
            if name == '学习阶段':
                cnt_round.set(f'肝数:{int(cnt_round.get()[3:]) + 1}')
        if name == '养肝阶段':
            Thread(target=livers, daemon=True).start()

    def run():
        st = 0
        before_update = update
        for i in range(int(smallNum) - 1):
            t1 = Timer(st * 60, partial(stage, name='学习阶段', t=studyTime, before_update=update))
            t1.start()
            st += int(studyTime)
            t2 = Timer(st * 60, partial(stage, name='休息阶段', t=smallTime, before_update=update))
            t2.start()
            st += int(smallTime)

        Timer(st * 60, partial(stage, name='学习阶段', t=studyTime, before_update=update)).start()
        st += int(studyTime)
        Timer(st * 60, partial(stage, name='休息阶段', t=bigTime, before_update=update)).start()
        st += int(bigTime)
        time.sleep(st * 60)
        if update == before_update:
            if isLoop.get() == 1:
                Thread(target=run, daemon=True).start()


    #Thread(target=run, daemon=True).start()

    #新增10点半养肝功能

    def livers(right_now=False):
        if right_now:
            Timer(3, partial(stage, name='养肝阶段', t=60, before_update=update)).start()
        now = datetime.datetime.now()
        h = now.time().hour
        m = now.time().minute
        liver_time = liver.split(":");
        liver_end = liver_to.split(":");
        th, tm = int(liver_time[0]), int(liver_time[1])
        eh, em = int(liver_end[0]), int(liver_end[1])

        target = datetime.datetime(now.year, now.month, now.day, th, tm, 0, 0)
        target_end = datetime.datetime(now.year, now.month, now.day, eh, em, 0, 0)
        print((target_end - now).seconds)
        if (h > th or h == th and m >= tm) and (h < eh or h == eh and m <= em):
            Timer(0, partial(stage, name='养肝阶段', t=(target_end - now).seconds // 60, before_update=update)).start()
        else:
            d = (target - now)
            Timer(d.seconds, partial(stage, name='养肝阶段', t=(target_end - target).seconds // 60, before_update=update)).start()

    def break_now():
        livers(right_now=True)



    Thread(target=livers, daemon=True).start()

    def close():
        if force:
            return
        while not end:
            time.sleep(1)
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
            data["isLoop"] = isLoop.get()
            #data["liver"] = liver
            #data["liver_to"] = liver_to
            #data["force"] = force
            #data["width"] = width
            #data["length"] = length
            #data["is_music"] = is_music
            json.dump(data, f, indent=3, ensure_ascii=False)


    root.protocol("WM_DELETE_WINDOW", quit_me)


    def login_clicked():
        """ callback when the login button clicked
        """
        global smallTime, bigTime, studyTime, smallNum
        msg = ''
        if not small.get().isdigit():
            msg = '小休息时间必须是数字！'
        elif not big.get().isdigit():
            msg = '大休息时间必须是数字！'
        elif not study.get().isdigit():
            msg = '学习时间必须是数字！'
        elif not smallNumVar.get().isdigit():
            msg = '小学次数必须是数字！'
        else:
            msg = f'修改成功'
            global update
            sm = int(small.get())
            b = int(big.get())
            st = int(study.get())
            sn = int(smallNumVar.get())
            max = 24 * 60
            if sm > max or b > max or st > max or sn > max:
                msg = '数字过大啦'
            elif sn <= 0:
                msg = '轮数必须大于1'
            else:
                smallTime = sm
                bigTime = b
                studyTime = st
                smallNum = sn
                update = update + 1
                Thread(target=run, daemon=True).start()

        showinfo(
            title='改变成功',
            message=msg
        )

    def pause_clicked():
        global pause
        pause = not pause
        if pause:
            pauseVar.set('取消暂停')
        else:
            pauseVar.set('暂停')

    def break_clicked():
        global update
        update = update + 1
        Thread(target=break_now, daemon=True).start()



    # Sign in frame
    signin = ttk.Frame(root)
    signin.pack(padx=10, pady=10, fill='x', expand=True)

    email_label = ttk.Label(signin, textvariable=stageInfoVar)
    email_label.pack(fill='x', expand=True)

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

    email_label = ttk.Label(signin, text="学习次数")
    email_label.pack(fill='x', expand=True)

    email_entry = ttk.Entry(signin, textvariable=smallNumVar)
    email_entry.pack(fill='x', expand=True)
    email_entry.focus()

    # login button
    login_button = ttk.Button(signin, text="确认修改", command=login_clicked)
    login_button.pack(fill='x', expand=True, pady=8)
    #
    # pause_button = ttk.Button(signin, textvariable=pauseVar, command=pause_clicked)
    # pause_button.pack(fill='x', expand=True, pady=5)

    break_now_button = ttk.Button(signin, text="强制休息", command=break_clicked)
    break_now_button.pack(fill='x', expand=True, pady=5)


    Button1 = tk.Checkbutton(signin, text="永无止尽的x月",
                             variable=isLoop,
                             width=10)
    Button1.pack()
    count_round = ttk.Label(signin, textvariable=cnt_round)
    count_round.pack(fill='x', expand=True)

    root.mainloop()
