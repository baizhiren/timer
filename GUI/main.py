import json
import time
import tkinter as tk
import datetime
from functools import partial
from threading import Thread, Timer
from tkinter import ttk
from tkinter.messagebox import showinfo
import pyautogui as ui
import os


from breakTimer.SystemMusic import SystemMusic

ui.FAILSAFE = False


if __name__ == '__main__':
    # multiprocessing.freeze_support()

    print("自动启动时的环境变量：", os.environ)
    print("自动启动时的环境变量：", os.environ.get('PYTHONPATH'))
    work_dir = os.getcwd()
    print("自动启动时的当前工作目录：", work_dir)

    user_dir = os.environ['USERPROFILE'] + '\\.breakTimer'
    config_path = user_dir + '\\location.txt'
    print('config_path: ',config_path)

    os.makedirs(user_dir, exist_ok=True)

    try:
        with open(config_path, 'r') as file:
            path = file.read()
            print('read path:', path)
    except:
        with open(config_path, 'w') as file:
            path = os.getcwd() + '\\config.json'
            file.write(path)


    root = tk.Tk()
    #size = "8000x3000+-4000+0"
    #size = "400x400+500+500"
    root.resizable(False, False)
    root.title('休息定时器3.2')

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

    smallTime = 1
    bigTime = 12
    studyTime = 40
    smallNum = 3
    is_loop = 1
    liver = "22:30"
    liver_to = "6:00"
    force = 1
    width = "450"
    length = "450"

    wx = "500"
    wy = "500"


    is_music = 0
    auto_start = 0
    debug = False

    target = ''
    target_end = ''
    now = ''
    if not debug:
        time.sleep(5)

    def write_configs(write_all=True, first_read=True):
        data = read_configs(first_read)
        global studyTime
        try:
            with open(path, "w", encoding="utf-8") as f:
                data["smallTime"] = smallTime
                data["bigTime"] = bigTime
                data["studyTime"] = studyTime
                data["smallNum"] = smallNum
                data["isLoop"] = isLoop.get()
                if target != '':
                    data['target'] = target.strftime("%Y-%m-%d %H:%M:%S")
                if target_end != '':
                    data['target_end'] = target_end.strftime("%Y-%m-%d %H:%M:%S")
                if write_all:
                    data["liver"] = liver
                    data["liver_to"] = liver_to
                    data["force"] = force
                    data["width"] = width
                    data["length"] = length
                    data["is_music"] = is_music
                    data["auto_start"] = auto_start
                json.dump(data, f, indent=3, ensure_ascii=False)
        except:
            print(f'写错误 write_all:{write_all} first read:{first_read}')

    def read_configs(first_read=True):
        global smallTime, bigTime, studyTime, smallNum, is_loop, liver, liver_to, force, width, length, is_music, target, target_end,path, auto_start
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)  # 加载我们的数据
                if first_read:
                    smallTime = data.get('smallTime', smallTime)
                    bigTime = data.get('bigTime', bigTime)
                    studyTime = data.get('studyTime', studyTime)
                    smallNum = data.get('smallNum', smallNum)
                    is_loop = data.get('isLoop', isLoop)
                    target = data.get('target', target)
                    try:
                        if target != '':
                            target = datetime.datetime.strptime(target, "%Y-%m-%d %H:%M:%S")

                        target_end = data.get('target_end', target_end)
                        if target_end != '':
                            target_end = datetime.datetime.strptime(target_end, "%Y-%m-%d %H:%M:%S")
                    except:
                        target = ''
                        target_end = ''
                liver = data.get('liver', liver)
                liver_to = data.get('liver_to', liver)
                force = data.get('force', force)
                width = data.get('width', width)
                length = data.get('length', length)
                is_music = data.get('is_music', is_music)
                auto_start = data.get('auto_start', auto_start)
                # path = data.get('path', path)

                return data
        except:
            print(f'读错误 first read:{first_read}')
            return {}

    #read_configs()
    write_configs(write_all=True, first_read=True)
    small.set(smallTime)
    big.set(bigTime)
    study.set(studyTime)
    smallNumVar.set(smallNum)
    isLoop.set(is_loop)
    size = width + "x" + length + "+" + wx + "+" + wy
    root.geometry(size)


    update = 0
    end = True
    lastEnd = True
    pause = False

    now_state = ''

    # 1 1 2 1 2 1
    def stage(name, t, before_update):
        print(f"hello, this is stage {name}, continue {t}")
        global end, lastEnd, update

        if before_update != update and name != '养肝阶段':
            return
        if name == '养肝阶段':
            update = update + 1

        while not lastEnd:
            time.sleep(1)
        global now_state
        now_state = name

        lastEnd = False
        if not debug:
            t = t * 60
        fullStage = ['休息阶段', '养肝阶段', '立刻休息']
        if name in fullStage:
            end = False
            if not debug:
                root.attributes('-topmost', 1)
            print('启动check window position')
            Thread(target=check_window_position(), daemon=True).start()
            if force:
                root.attributes('-fullscreen', True)
            root.deiconify()
            login_button.configure(state='disable')
            break_now_button.configure(state='disable')

        global stageInfo
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
        if name == '休息阶段' or name == '立刻休息':
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


    def run():
        if not debug:
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
        else:
            st = 0
            before_update = update
            for i in range(int(smallNum) - 1):
                t1 = Timer(st, partial(stage, name='学习阶段', t=studyTime, before_update=update))
                t1.start()
                st += int(studyTime)
                t2 = Timer(st, partial(stage, name='休息阶段', t=smallTime, before_update=update))
                t2.start()
                st += int(smallTime)

            Timer(st, partial(stage, name='学习阶段', t=studyTime, before_update=update)).start()
            st += int(studyTime)
            Timer(st, partial(stage, name='休息阶段', t=bigTime, before_update=update)).start()
            st += int(bigTime)
            time.sleep(st)

        if update == before_update:
            if isLoop.get() == 1:
                Thread(target=run, daemon=True).start()





    if auto_start:
        Thread(target=run, daemon=True).start()

    def break_now():
        Timer(3, partial(stage, name='立刻休息', t=60, before_update=update)).start()

    def check():
        now = datetime.datetime.now()
        return (now >= target) and (now <= target_end)

    def update_target(firstTime=True):
        global target, target_end
        now = datetime.datetime.now()
        if target != '' and target_end != '' and now <= target_end:
            return
        if target != '' and target.day == now.day:
            return
        liver_time = liver.split(":");
        liver_end = liver_to.split(":");
        th, tm = int(liver_time[0]), int(liver_time[1])
        eh, em = int(liver_end[0]), int(liver_end[1])
        target = datetime.datetime(now.year, now.month, now.day, th, tm, 0, 0)
        target_end = datetime.datetime(now.year, now.month, now.day, eh, em, 0, 0)
        if not (eh > th or eh == th and em >= tm):
            one_day = datetime.timedelta(days=1)
            target_end = target_end + one_day
        write_configs(write_all=False, first_read=False)

    update_target(firstTime=True)




    # 实时监控
    def monitor():
        print('monitor 启动' + target.strftime("%Y-%m-%d %H:%M:%S"))
        # time.sleep(1)
        global end
        global now_state
        gap_time = 5
        Timer(gap_time * 60, monitor).start()
        if check():
            stage(name='养肝阶段', t=gap_time, before_update=update)
        elif now_state == '养肝阶段':
            root.attributes('-fullscreen', False)
            root.geometry(size)
            root.attributes('-topmost', 0)
            end = True
            login_button.configure(state='enable')
            break_now_button.configure(state='enable')
            now_state = ''
            update_target(firstTime=False)
        else:
            if now_state == '' and auto_start:
                Thread(target=run, daemon=True).start()
            update_target(firstTime=False)


    def check_window_position():
        window_x = root.winfo_x()
        window_y = root.winfo_y()
        if window_x != 0 or window_y != 0:
            root.attributes('-fullscreen', False)
            root.attributes('-fullscreen', True)
            print('错位重置')
        if not end:
            root.after(1000, check_window_position)
        else:
            root.attributes('-fullscreen', False)


    # Thread(target=livers, daemon=True).start()
    Thread(target=monitor, daemon=True).start()


    def close():
        if force:
            return
        while not end:
            time.sleep(1)
        root.quit()
        global update
        update = update + 1

    def quit_me():
        write_configs(write_all=False, first_read=False)
        Timer(0, close).start()

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

    break_now_button = ttk.Button(signin, text="强制休息", command=break_clicked)
    break_now_button.pack(fill='x', expand=True, pady=5)


    Button1 = tk.Checkbutton(signin, text="永无止尽的x月",
                             variable=isLoop,
                             width=10)
    Button1.pack()
    count_round = ttk.Label(signin, textvariable=cnt_round)
    count_round.pack(fill='x', expand=True)

    root.mainloop()
