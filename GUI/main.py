import json
import time
import tkinter as tk
import datetime
from functools import partial
from threading import Thread, Timer
from tkinter import ttk
from tkinter.messagebox import showinfo
import pyautogui as ui

from tkinter import *

import winreg
import os

import sys

# 要添加到自启动的应用程序名称和路径
app_name = "breakTimer3.7"

# 打开注册表键


from breakTimer.SystemMusic import SystemMusic
from breakTimer.BlackSheet import BlackSheet

ui.FAILSAFE = False

import logging


def redirect_print_to_log(log_file_path):
    # 创建日志记录器
    logger = logging.getLogger('print_logger')
    logger.setLevel(logging.INFO)

    # 创建文件处理器
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将文件处理器添加到日志记录器
    logger.addHandler(file_handler)

    # 重定向print语句的输出
    class PrintToLog:
        def write(self, message):
            if message.rstrip() != '':
                logger.info(message.rstrip())

    # 将标准输出重定向到PrintToLog对象
    print_to_log = PrintToLog()
    sys.stdout = print_to_log


if __name__ == '__main__':
    # multiprocessing.freeze_support()
    try:
        debug = True
        if getattr(sys, 'frozen', False):
            # 在可执行文件中运行的逻辑
            print("在可执行文件中运行")
            debug = False

        # print("自动启动时的环境变量：", os.environ)
        # print("自动启动时的环境变量：", os.environ.get('PYTHONPATH'))
        work_dir = os.getcwd()
        print("自动启动时的当前工作目录：", work_dir)

        user_dir = os.environ['USERPROFILE'] + '\\.breakTimer'
        if not debug:
            redirect_print_to_log(user_dir + "\\output.log")

        config_path = user_dir + '\\location.txt'
        print('config_path: ', config_path)

        os.makedirs(user_dir, exist_ok=True)

        try:
            with open(config_path, 'r') as file:
                path = file.read()
                print('read path:', path)
        except:
            with open(config_path, 'w') as file:
                path = work_dir + '\\config.json'
                file.write(path)

        root = tk.Tk()
        root.resizable(False, False)
        root.title(app_name)

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
        is_loop = 1
        liver = "22:30"
        liver_to = "6:00"
        force = 0

        width = "450"
        length = "450"

        v_ = {
            "fast_start": 1,
            "split_screen": 1,
            "mouse_lock": 1,
            "auto_boot": 1,
            "break_now_time": 20,
            "black_list_open": 1,
            "mode": 'study',
            "black_lists": {
                "study": ['msedge.exe', 'steam.exe', "chrome.exe"],
                "fun": [],
            }
        }

        wx = "500"
        wy = "500"

        is_music = 0
        auto_start = 1

        target = ''
        target_end = ''
        now = ''
        destory = False


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
                        for str_name, name in v_.items():
                            data[str_name] = name
                    json.dump(data, f, indent=3, ensure_ascii=False)
            except:
                print(f'写错误 write_all:{write_all} first read:{first_read}')


        def read_configs(first_read=True):
            global smallTime, bigTime, studyTime, smallNum, is_loop, liver, liver_to, force, width, length, is_music, target, target_end, path, auto_start
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)  # 加载我们的数据
                    # 这些可以实时更新（在程序里更新
                    if first_read:
                        smallTime = data.get('smallTime', smallTime)
                        bigTime = data.get('bigTime', bigTime)
                        studyTime = data.get('studyTime', studyTime)
                        smallNum = data.get('smallNum', smallNum)
                        is_loop = data.get('isLoop', isLoop)
                        try:
                            target = data.get('target', target)
                            if target != '':
                                target = datetime.datetime.strptime(target, "%Y-%m-%d %H:%M:%S")

                            target_end = data.get('target_end', target_end)
                            if target_end != '':
                                target_end = datetime.datetime.strptime(target_end, "%Y-%m-%d %H:%M:%S")
                        except:
                            target = ''
                            target_end = ''
                    # 这些不可以实时更新
                    liver = data.get('liver', liver)
                    liver_to = data.get('liver_to', liver_to)
                    force = data.get('force', force)
                    width = data.get('width', width)
                    length = data.get('length', length)
                    is_music = data.get('is_music', is_music)
                    auto_start = data.get('auto_start', auto_start)
                    for str_name, v in v_.items():
                        v_[str_name] = data.get(str_name, v)
                    return data
            except:
                print(f'读错误 first read:{first_read}')
                return {}


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

        if v_["auto_boot"]:
            app_path = work_dir + "\\breakTimer.exe"
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                value, value_type = winreg.QueryValueEx(reg, app_name)
                print(value, value_type)
                winreg.CloseKey(reg)
                print('自启项已存在')
            except:
                try:
                    with winreg.OpenKey(key, key_path, 0, winreg.KEY_ALL_ACCESS) as reg_key:
                        # 设置自启动项
                        winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, app_path)
                    print('设置应用启动项成功')
                except Exception as e:
                    print('设置应用自启项失败', e)

            # 检测是否被移除自启动
            try:
                # 打开注册表
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                         r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run", 0,
                                         winreg.KEY_ALL_ACCESS)
                # 如果键存在，删除它
                winreg.DeleteValue(reg_key, app_name)
                winreg.CloseKey(reg_key)
                print("删除被禁用成功")
            except Exception as e:
                print("删除被禁用失败:", e)
        else:
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                         r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                                         winreg.KEY_ALL_ACCESS)
                # 如果键存在，删除它
                winreg.DeleteValue(reg_key, app_name)
                winreg.CloseKey(reg_key)
                print("应用取消自启")
            except Exception as e:
                print("应用取消自启失败", e)

        if not v_["fast_start"] and force:
            time.sleep(5)

        fullStage = ['休息阶段', '大休息阶段', '养肝阶段', '立刻休息']

        from screeninfo import get_monitors

        sub_screen_array = []
        before_monitors = ''


        def span():
            monitors = get_monitors()
            global before_monitors
            before_monitors = monitors
            for m in monitors:
                if m.x != 0 or m.y != 0:
                    sub_screen = Toplevel()
                    sub_screen.geometry('%dx%d+%d+%d' % (m.width, m.height, m.x, m.y))
                    create_clock(sub_screen)
                    sub_screen.attributes('-topmost', 1)
                    sub_screen.overrideredirect(1)
                    sub_screen_array.append(sub_screen)


        def destroy_sub_screen():
            global sub_screen_array
            for sub_screen in sub_screen_array:
                sub_screen.destroy()
            sub_screen_array = []


        click_update = False
        blackSheet = None


        def stage(name, t, before_update):
            global end, lastEnd, update, click_update, blackSheet
            print(f"hello, this is stage {name}, continue {t}, before update:{before_update}, now update: {update}")

            if before_update != update and name != '养肝阶段' or destory:
                print(f"expire {name}, before update:{before_update} now update: {update}")
                return
            if name == '养肝阶段':
                update = update + 1

            if not lastEnd:
                print(f'{name}等待前一个阶段ing')
            while not lastEnd:
                time.sleep(1)

            global now_state
            if name == '养肝阶段' and before_update + 100 <= update:
                return
            now_state = name
            lastEnd = False

            if not debug:
                t = t * 60
            if name in fullStage:
                end = False
                root.attributes('-topmost', 1)
                if force:
                    root.attributes('-fullscreen', True)
                root.deiconify()
                login_button.configure(state='disable')
                break_now_button.configure(state='disable')
                reload_button.configure(state='disable')

                if v_["split_screen"] and force:
                    span()
            # 保险
            elif root.attributes('-fullscreen'):
                root.attributes('-topmost', 0)
                root.attributes('-fullscreen', False)

            if v_['black_list_open'] and name == '学习阶段':
                if blackSheet:
                    blackSheet.start()
                black_lists = v_["black_lists"]
                black_list = None
                try:
                    black_list = black_lists[v_["mode"]]
                except:
                    pass
                if black_list:
                    # 如果不是always模式，只有按下确认修改按钮后的几轮是有黑名单的
                    if black_list[-1] == "always" or click_update:
                        blackSheet = BlackSheet(black_list)
                        blackSheet.start()
                        print(f'开启{v_["mode"]}黑名单')
                        reload_button.configure(state='disable')


            global stageInfo
            for i in range(t):
                if before_update != update and name != '养肝阶段':
                    print(f"expire {name} in the loop, before update:{before_update} now update: {update}")
                    break
                stageInfo = f'当前阶段:{name}  剩余时间:  {t // 60}分 : {t % 60}秒'
                if destory:
                    return
                stageInfoVar.set(stageInfo)
                if name in fullStage:
                    if not end:
                        Thread(name='p1', target=check_window_position, daemon=True).start()
                    else:
                        break
                time.sleep(1)
                t = t - 1
                while pause:
                    time.sleep(1)
            stageInfoVar.set(f'当前阶段:{name}  剩余时间: 0分 : 0秒')
            if name in fullStage and name != '养肝阶段':
                exit_full_stage()
                if not blackSheet:
                    reload_button.configure(state='enable')
                if name == '大休息阶段' or name == '立刻休息':
                    click_update = False
                    reload_button.configure(state='enable')
                    blackSheet = None

            lastEnd = True
            if blackSheet:
                blackSheet.stop()
                # reload_button.configure(state='enable')

            if before_update == update:
                if is_music:
                    music.ring(n=2)
                if name == '学习阶段':
                    cnt_round.set(f'肝数:{int(cnt_round.get()[3:]) + 1}')


        def exit_full_stage():
            global end
            root.attributes('-fullscreen', False)
            root.geometry(size)
            root.attributes('-topmost', 0)
            end = True
            login_button.configure(state='enable')
            break_now_button.configure(state='enable')
            destroy_sub_screen()


        def check():
            now = datetime.datetime.now()
            return (now >= target) and (now <= target_end)


        def run():
            if not debug:
                st = 0
                before_update = update
                for i in range(int(smallNum) - 1):
                    t1 = Timer(st * 60, partial(stage, name='学习阶段', t=studyTime, before_update=before_update))
                    t1.daemon = True
                    t1.start()
                    st += int(studyTime)
                    t2 = Timer(st * 60, partial(stage, name='休息阶段', t=smallTime, before_update=before_update))
                    t2.daemon = True
                    t2.start()

                    st += int(smallTime)

                t3 = Timer(st * 60, partial(stage, name='学习阶段', t=studyTime, before_update=before_update))
                t3.daemon = True
                t3.start()

                st += int(studyTime)
                t4 = Timer(st * 60, partial(stage, name='大休息阶段', t=bigTime, before_update=before_update))
                t4.daemon = True
                t4.start()
                st += int(bigTime)
                time.sleep(st * 60)
            else:
                st = 0
                before_update = update
                studyTime_d = 10
                smallTime_d = 8
                bigTime_d = 8
                smallNum_d = 2

                for i in range(int(smallNum_d) - 1):
                    t1 = Timer(st, partial(stage, name='学习阶段', t=studyTime_d, before_update=before_update))
                    t1.daemon = True
                    t1.name = 't1'
                    t1.start()

                    st += int(studyTime_d)
                    t2 = Timer(st, partial(stage, name='休息阶段', t=smallTime_d, before_update=before_update))
                    t2.daemon = True
                    t2.name = 't2'
                    t2.start()
                    st += int(smallTime_d)

                t3 = Timer(st, partial(stage, name='学习阶段', t=studyTime_d, before_update=before_update))
                t3.daemon = True
                t3.name = 't3'
                t3.start()

                st += int(studyTime_d)
                t4 = Timer(st, partial(stage, name='大休息阶段', t=bigTime_d, before_update=before_update))
                t4.daemon = True
                t4.name = 't4'
                t4.start()
                st += int(bigTime_d)
                time.sleep(st)

            # show_all_threads()

            if update == before_update:
                if not destory and isLoop.get() == 1:
                    Thread(name='p2', target=run, daemon=True).start()


        if auto_start:
            Thread(name='p3', target=run, daemon=True).start()


        def break_now():
            t = Timer(3, partial(stage, name='立刻休息', t=v_["break_now_time"], before_update=update))
            t.name = 'ta'
            t.start()


        def update_first_time_target():
            global target, target_end
            now = datetime.datetime.now()
            if target != '' and target_end != '' and now <= target_end:
                return
            # 对应定时任务不存在或者已经过期
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
            print('new target:', 'target', target, ' target end:', target_end)


        def update_target():
            global target, target_end
            one_day = datetime.timedelta(days=1)
            target_end = target_end + one_day
            target = target + one_day
            write_configs(write_all=False, first_read=False)


        update_first_time_target()


        # 实时监控
        def monitor():
            print(f'monitor 启动: '
                  f'target start:{target.strftime("%Y-%m-%d %H:%M:%S")}\n'
                  f'target end:{target_end.strftime("%Y-%m-%d %H:%M:%S")}\n'
                  f'now:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            global end
            global now_state
            global update
            gap_time = 5
            if debug:
                gap_time = 15
            if not debug:
                Timer(gap_time * 60, monitor).start()
            elif not destory:
                t5 = Timer(gap_time, monitor)
                t5.name = 't5'
                t5.start()

            if check():
                stage(name='养肝阶段', t=gap_time, before_update=update)
            elif now_state == '养肝阶段':
                print('退出养肝阶段 ...')
                exit_full_stage()
                reload_button.configure(state='enable')
                now_state = ' '
                destroy_sub_screen()
                update = update + 100
                if auto_start:
                    Thread(name='p4', target=run, daemon=True).start()
                update_target()


        def check_window_position():
            if force and now_state in fullStage:
                if v_["split_screen"]:
                    monitors = get_monitors()
                    if len(monitors) != len(before_monitors):
                        destroy_sub_screen()
                        span()
                    for m1, m2 in zip(monitors, before_monitors):
                        if m1.width != m2.width or m1.height != m2.height or m1.x != m2.x or m1.y != m2.y:
                            destroy_sub_screen()
                            span()
                if v_["mouse_lock"]:
                    ui.moveTo(0, 0)
                    ui.click()
                window_x = root.winfo_x()
                window_y = root.winfo_y()
                if window_x != 0 or window_y != 0:
                    root.attributes('-fullscreen', False)
                    root.attributes('-fullscreen', True)
                    print('错位重置')


        Thread(name='p5', target=monitor, daemon=True).start()


        # from tools.printThread import show_all_threads
        def close():
            if force:
                return
            global destory
            destory = True
            if blackSheet:
                blackSheet.stop()
            time.sleep(1)
            destroy_sub_screen()
            # show_all_threads()
            try:
                root.destroy()
                print('主线程结束')
            except Exception as e:
                print(e)


        def quit_me():
            write_configs(write_all=False, first_read=False)
            close()


        root.protocol("WM_DELETE_WINDOW", quit_me)


        def start_study(using_black_list=True):
            global click_update
            click_update = using_black_list
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
                    Thread(name='p6', target=run, daemon=True).start()

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
            Thread(name='p7', target=break_now, daemon=True).start()


        # Sign in frame
        def create_clock(root):
            clock = ttk.Frame(root)
            clock.pack(padx=10, pady=10, fill='x', expand=True)

            email_label = ttk.Label(clock, textvariable=stageInfoVar)
            email_label.pack(fill='x', expand=True)

            email_label = ttk.Label(clock, text="小休时间")
            email_label.pack(fill='x', expand=True)

            email_entry = ttk.Entry(clock, textvariable=small)
            email_entry.pack(fill='x', expand=True)
            email_entry.focus()

            password_label = ttk.Label(clock, text="大休时间:")
            password_label.pack(fill='x', expand=True)

            password_entry = ttk.Entry(clock, textvariable=big)
            password_entry.pack(fill='x', expand=True)

            email_label = ttk.Label(clock, text="学习时间")
            email_label.pack(fill='x', expand=True)

            email_entry = ttk.Entry(clock, textvariable=study)
            email_entry.pack(fill='x', expand=True)
            email_entry.focus()

            email_label = ttk.Label(clock, text="学习次数")
            email_label.pack(fill='x', expand=True)

            email_entry = ttk.Entry(clock, textvariable=smallNumVar)
            email_entry.pack(fill='x', expand=True)
            email_entry.focus()

            return clock


        clock1 = create_clock(root)
        login_button = ttk.Button(clock1, text="开始自律", command=start_study)
        login_button.pack(fill='x', expand=True, pady=8)

        break_now_button = ttk.Button(clock1, text="强制休息", command=break_clicked)
        break_now_button.pack(fill='x', expand=True, pady=5)

        frame = tk.Frame(clock1)
        frame.pack(pady=10)

        reload_button = ttk.Button(frame, text="重置", command=lambda: start_study(using_black_list=False))
        reload_button.pack(side='left', padx=10)

        loop_button = ttk.Checkbutton(frame, text="永无止尽的x月",
                                      variable=isLoop)
        loop_button.pack(padx=10, side='left')

        count_round = ttk.Label(frame, textvariable=cnt_round)
        count_round.pack(fill='x', expand=True, side = 'left', padx=10)

        root.mainloop()
    except Exception as e:
        print('未知异常', e)
