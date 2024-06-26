import ctypes
import json
import time
import tkinter as tk
import datetime
import traceback
from functools import partial
from threading import Thread, Timer
from tkinter import ttk
from tkinter.messagebox import showinfo
from typing import Dict

import keyboard
import pyautogui as ui

from tkinter import *

import winreg
import os

import sys

# 要添加到自启动的应用程序名称和路径
from breakTimer.Component import Component
from breakTimer.DelayBreak import DelayBreak
from breakTimer.FileChecker import FileChecker
from breakTimer.Hook import Hook

app_name = "breakTimer3.9.7"

# 打开注册表键


from breakTimer.SystemMusic import SystemMusic
from breakTimer.BlackSheet import BlackSheet
from breakTimer.BlockKeyboard import BlockKeyBoard
from breakTimer.BlockWebsite import BlockWebsite
from breakTimer.ModifyProxyOption import ModifyProxyOption
from breakTimer.WhiteSheet import WhiteSheet
from breakTimer.LeaveDetect import LeaveDetect

ui.FAILSAFE = False
['正常', '学习', '短', '休息', '超短']
debug_mode = '休息'

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


def create_if_not_exist(file_path):
    if not os.path.exists(file_path):
        # 文件不存在，创建文件并写入内容
        with open(file_path, "w") as file:
            file.write("")
        print(f"文件 '{file_path}' 不存在，已创建文件。")
    else:
        # 文件已存在，不做任何操作
        print(f"文件 '{file_path}' 已存在，不做任何操作。")




if __name__ == '__main__':
    # multiprocessing.freeze_support()

    try:
        debug = True
        if getattr(sys, 'frozen', False):
            # 在可执行文件中运行的逻辑
            print("在可执行文件中运行")
            debug = False
        else:
            print('debug模式启动')
        # debug = True

        # print("自动启动时的环境变量：", os.environ)
        # print("自动启动时的环境变量：", os.environ.get('PYTHONPATH'))
        user_dir = os.environ['USERPROFILE'] + '\\.breakTimer'
        log_dir = user_dir + "\\output.log"

        work_dir = os.getcwd()


        config_path = user_dir + '\\location.txt'


        os.makedirs(user_dir, exist_ok=True)
        create_if_not_exist(log_dir)

        if not debug:
            redirect_print_to_log(user_dir + "\\output.log")

        print("自动启动时的当前工作目录：", work_dir)
        print('config_path: ', config_path)

        try:
            with open(config_path, 'r') as file:
                path = file.read()
                print('read path:', path)
        except:
            with open(config_path, 'w') as file:
                path = work_dir + '\\config.json'
                file.write(path)

        proxy_path = os.environ['USERPROFILE'] + r"//.config/clash/profiles"
        print("proxy_path", proxy_path)
        import os
        # proxy_path

        print('proxy_path', proxy_path)

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
        force = 1

        if not debug:
            force = 1
        else:
            force = 0
        width = "500"
        length = "480"
        g_ = {
        }

        v_ = {
            "fast_start": 1,
            "split_screen": 1,
            "mouse_lock": 1,
            "auto_boot": 1,
            "break_now_time": 20,
            "block_keyboard": 1,
            "full_screen": 1,
            "lock_screen_when_start_rest": 1,
            "topmost": 1,
            "leave_restart": 1,
            "pause_current_app_when_break": 1,
            "delay_break": 1,
            "check_window_position": 1,
            "monitor_gap": 1,
            "black_lists": [
                {
                    "name": "study",
                    "list": [
                        "msedge.exe",
                        "steam.exe",
                        "chrome.exe"
                    ],
                    "enable": 0,
                    "time": {
                        "mode": "click"
                    }
                },
                {
                    "name": "test",
                    "list": [
                        "chrome.exe"
                    ],
                    "enable": 0,
                    "time": {
                        "mode": "day",
                        "interval": "11:00-12:30"
                    }
                }
            ],
            "block_website": {
                "enable": 0,
                "proxy_rules_location": "C:\\Users\\chao//.config/clash/profiles",
                "websites": [
                    {
                        "name": "zhihu.com",
                        "time": {
                            "mode": "period",
                            "interval": "2024.2.22 14:00-2024.2.22 23:00"
                        },
                        "enable": 1
                    }
                ]
            },
            "white_sheet": [
                {
                    "mode": "period",
                    "interval": "2024.2.21 10:00-2024.2.21 10:10"
                }
            ]
        }

        wx = "500"
        wy = "500"

        is_music = 0
        auto_start = 1

        target = ''
        target_end = ''
        now = ''
        destory = False
        block_website = None


        class JsonWriter(Component, Hook):
            def __init__(self, cls, **kwargs):
                Hook.__init__(self, cls, **kwargs)
                super().__init__(name='jsonWriter')

            def start_fish(self):
                global block_website
                pre_block_enable = v_["block_website"]["enable"]

                write_configs(False, False)
                # 做一些热更新
                # 1. block website的网站更新
                if block_website:
                    block_website.websites = v_["block_website"]["websites"]

                if pre_block_enable == 0 and v_["block_website"]["enable"] == 1:
                    block_website = BlockWebsite(block_websites=v_["block_website"]["websites"],
                                                 dir=v_["block_website"]["proxy_rules_location"])
                    Thread(name='网页阻止', target=block_website.start, daemon=True).start()
                    print('**代理服务器开启')
                if pre_block_enable == 1 and v_["block_website"]["enable"] == 0:
                    block_website.stop()
                    print('**关闭代理服务器！')


                # 2. 白名单更新
                # print(f'已读取新配置config{v_}')


        jsonWriter = JsonWriter(FileChecker, **{'path': path, 'fish_name': 'config file checker'})


        def update_config(key, value):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)  # 加载我们的数据
            data[key] = value
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=3, ensure_ascii=False)


        def write_configs(write_all=True, first_read=True):
            print(f'调用write config at {datetime.datetime.now()}')
            jsonWriter.fish.add()
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
                    for str_name, name in g_.items():
                        data[str_name] = name
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
                        is_loop = data.get('isLoop', is_loop)
                        isLoop.set(is_loop)
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

                        for str_name, v in g_.items():
                            g_[str_name] = data.get(str_name, v)

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
        jsonWriter.start()

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
        #作弊
        if debug:
            #v_["full_screen"] = 0
            v_["mouse_lock"] = 0
            #v_["lock_screen_when_start_rest"] = 0
            v_["topmost"] = 0
            v_["leave_restart"] = 1
            v_["block_keyboard"] = 0
            # force = 0
            if debug_mode == '正常':
                studyTime = 15
                smallTime = 15
                bigTime = 15
                smallNum = 3
            elif debug_mode == '学习':
                studyTime = 20
                smallTime = 5
                bigTime = 10
                smallNum = 3
            elif debug_mode == '超短':
                studyTime = 3
                smallTime = 3
                bigTime = 3
                smallNum = 2
            elif  debug_mode == '休息':
                studyTime = 5
                smallTime = 20
                bigTime = 25
                smallNum = 3
            elif debug_mode == '短':
                studyTime = 8
                smallTime = 8
                bigTime = 8
                smallNum = 3

            pass

        if v_["auto_boot"]:
            app_path = work_dir + "\\breakTimer.exe"
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)

                def delete_matching_registry_values(key_path, pattern):
                    # 打开指定路径的注册表键
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                        i = 0
                        while True:
                            try:
                                # 枚举键中的每一个值
                                value_name, value_data, value_type = winreg.EnumValue(key, i)
                                # 检查值的名称是否符合模式
                                if value_name.startswith(pattern) and value_name != app_name:
                                    print(f"Deleting: {value_name}")
                                    winreg.DeleteValue(key, value_name)
                                else:
                                    i += 1
                            except OSError:
                                # 当索引超出范围时，停止遍历
                                break
                # 使用函数，指定键路径和要匹配的模式
                pattern = 'breakTimer'
                delete_matching_registry_values(key_path, pattern)
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
                    if v_["topmost"]:
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
        block_keyboard = None
        lock_screen_flag = False


        def start_stage(stage):
            global end, lastEnd, update, click_update, blackSheet, block_keyboard, lock_screen_flag
            name = stage.name
            t = stage.time
            before_update = stage.before_update

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

            # 这里制定休息模式规则
            white_sheet_open = False
            pause_open = False

            if name in fullStage:
                end = False
                pause_open = False
                whiteSheet = WhiteSheet(v_["white_sheet"])
                white_list, flag = whiteSheet.get_new_white_sheet()
                delayBreak = None
                if flag:
                    v_["white_sheet"] = white_list
                    update_config("white_sheet", v_["white_sheet"])
                if not whiteSheet.todo() or name == '养肝阶段':
                    if v_["topmost"]:
                        root.attributes('-topmost', 1)
                    if force:
                        if v_["full_screen"]:
                            root.attributes('-fullscreen', True)
                            if v_["split_screen"]:
                                # split_screen_timer = Timer(1, span)
                                # split_screen_timer.name = 'split screen in the loop span'
                                # split_screen_timer.daemon = True
                                span()
                                print('当前屏幕：', get_monitors())
                                print('增加多屏锁定1 full stage开启')
                        if v_["block_keyboard"]:
                            block_keyboard = BlockKeyBoard()
                            block_keyboard.start()
                        if v_["pause_current_app_when_break"]:
                            music.pause()
                            # pause_open = True

                    if v_["lock_screen_when_start_rest"] and not lock_screen_flag:
                        ctypes.windll.user32.LockWorkStation()
                        lock_screen_flag = True
                    if v_["topmost"]:
                        root.deiconify()

                    login_button.configure(state='disable')
                    break_now_button.configure(state='disable')
                    reload_button.configure(state='disable')
                    if not debug:
                        jump_button.configure(state='disable')
                    if name != '养肝阶段' and v_["delay_break"]:
                        func = partial(Execute.now_execute.insert_stage, info={'name': '学习阶段_临时', 'time': 5})
                        delayBreak = DelayBreak(func)
                        delayBreak.start()
                else:
                    white_sheet_open = True

            # 保险
            else:
                lock_screen_flag = False
                root.attributes('-topmost', 0)
                root.attributes('-fullscreen', False)
                if block_keyboard:
                    block_keyboard.stop()
            leaveDetect = None
            if name == '学习阶段_临时':
                login_button.configure(state='disable')
                reload_button.configure(state='disable')



            if '学习阶段' in name:
                if blackSheet:
                    blackSheet.start()
                black_lists = v_["black_lists"]
                blackSheet = BlackSheet(black_lists, click=click_update)
                blackSheet.start()
                if click_update:
                    reload_button.configure(state='disable')
                if v_["leave_restart"]:
                    def leave():
                        Execute.now_execute.stop()
                        keyboard.read_key()
                        Thread(name='在大休息阶段结束、立刻休息结束', target=run, daemon=True).start()
                    leaveDetect = LeaveDetect(leave, count_down=60 * 10, detect_keyboard_time=60)
                    if debug:
                        leaveDetect = LeaveDetect(leave, count_down=20, detect_keyboard_time=5)
                    leaveDetect.start()

            global stageInfo
            for i in range(t, 0, -1):
                if before_update != update and name != '养肝阶段':
                    print(f"expire {name} in the loop, before update:{before_update} now update: {update}")
                    break
                stageInfo = f'当前阶段:{name}  剩余时间:  {i // 60}分 : {i % 60}秒'
                if destory:
                    return
                stageInfoVar.set(stageInfo)
                if name in fullStage and not white_sheet_open:
                    if not end:
                        if v_["check_window_position"] and i > 2:
                            # print(f'check window position i={i}')
                            Thread(name='p1', target=check_window_position, daemon=True).start()
                    else:
                        break
                time.sleep(1)
                while pause:
                    time.sleep(1)
            stageInfoVar.set(f'当前阶段:{name}  剩余时间: 0分 : 0秒')
            if name in fullStage and name != '养肝阶段':
                exit_full_stage()
                if delayBreak:
                    delayBreak.stop()
                if not click_update:
                    reload_button.configure(state='enable')
                if name == '大休息阶段' or name == '立刻休息':
                    click_update = False
                    reload_button.configure(state='enable')
                    blackSheet = None
                    if update == before_update:
                        if not destory and isLoop.get() == 1:
                            print('大休息阶段 或者 立刻休息结束, 等待键盘输入')
                            keyboard.read_key()
                            Thread(name='在大休息阶段结束、立刻休息结束', target=run, daemon=True).start()
            if '学习阶段' in name:
                if leaveDetect:
                    leaveDetect.stop()

            lastEnd = True
            if blackSheet:
                blackSheet.stop()
                # reload_button.configure(state='enable')

            if before_update == update:
                if is_music:
                    music.ring(n=2)
                if name == '学习阶段':
                    cnt_round.set(f'肝数:{int(cnt_round.get()[3:]) + 1}')

        class Stage:
            def __init__(self):
                self.name = ''
                self.excute = None
                self.time = -1
                self.info = {}
                self.before_update = -1

            def start(self):
                start_stage(self)
                self.excute.next_stage_start()


            #暂停时间

        class Execute:

            now_execute = None

            def __init__(self, stages):
                Execute.now_execute = self
                self.stages = stages
                self.idx = 0
                self.before_update = update
                self.delay_count = 0;

            def next_stage_start(self):
                if self.idx >= len(self.stages):
                    return
                stage = self.new_Stage(self.stages[self.idx], before_update=update)
                self.idx += 1
                stage.start()

            def jump(self):
                global update
                update = update + 1

            def new_Stage(self, info: Dict[str, str], before_update):
                s = Stage()
                s.name = info["name"]
                s.time = info["time"]
                s.excute = self
                s.info = info
                s.before_update = before_update
                return s

            # 在当前阶段前插入一个阶段
            def insert_stage(self, info: Dict[str, str]):
                if self.delay_count >= 3:
                    return
                # 增加三分钟
                self.stages[self.idx - 1]['time'] += 3 # 休息模式+3
                self.stages.insert(self.idx - 1, info)
                self.idx = self.idx - 1
                self.jump()
                self.delay_count += 1;

            def stop(self):
                self.idx = len(self.stages)
                self.jump()




        def exit_full_stage(pause_open=False):
            global end, block_keyboard
            root.attributes('-fullscreen', False)
            root.geometry(size)
            root.attributes('-topmost', 0)
            end = True
            if v_["block_keyboard"] and block_keyboard:
                block_keyboard.stop()
                block_keyboard = None
            login_button.configure(state='enable')
            break_now_button.configure(state='enable')
            jump_button.configure(state='enable')
            destroy_sub_screen()
            if pause_open:
                music.pause()



        def check():
            now = datetime.datetime.now()
            return (now >= target) and (now <= target_end)


        def run():
            study_stage = {
                'name': '学习阶段',
                'time': studyTime,
            }
            break_stage = {
                'name': '休息阶段',
                'time': smallTime,
            }
            big_break_stage = {
                'name': '大休息阶段',
                'time': bigTime,
            }

            stages = []

            for i in range(int(smallNum) - 1):
                stages.append(study_stage.copy())
                stages.append(break_stage.copy())

            stages.append(study_stage.copy())
            stages.append(big_break_stage.copy())
            execute = Execute(stages)

            Thread(name='run', target=execute.next_stage_start, daemon=True).start()

            # show_all_threads()

            # if update == before_update:
            #     if not destory and isLoop.get() == 1:
            #         Thread(name='p2', target=run, daemon=True).start()


        if auto_start:
            Thread(name='p3', target=run, daemon=True).start()


        def break_now():
            Execute.now_execute.stop()
            break_now_stage = {
                'name': '立刻休息',
                'time': v_["break_now_time"],
            }
            stages = [break_now_stage]
            execute = Execute(stages)

            Thread(name='立刻休息', target=execute.next_stage_start, daemon=True).start()



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

        monitor_cnt = 0
        # 实时监控
        def monitor():
            global  monitor_cnt
            global end
            global now_state
            global update
            monitor_cnt += 1
            if monitor_cnt % 5 == 0:
                print(f'monitor 启动: '
                      f'target start:{target.strftime("%Y-%m-%d %H:%M:%S")}\n'
                      f'target end:{target_end.strftime("%Y-%m-%d %H:%M:%S")}\n'
                      f'now:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                print('当前状态：', now_state)

            gap_time = v_["monitor_gap"]
            if debug:
                gap_time = 15
                Timer(gap_time, monitor).start()
            else:
                if not destory:
                    Timer(gap_time * 60, monitor).start()

            if check():
                Execute.now_execute.stop()
                break_now_stage = {
                    'name': '养肝阶段',
                    'time': gap_time
                }
                stages = [break_now_stage]
                execute = Execute(stages)
                Thread(name='立刻休息', target=execute.next_stage_start, daemon=True).start()
            elif now_state == '养肝阶段':
                print('退出养肝阶段 ...')
                exit_full_stage()
                reload_button.configure(state='enable')
                now_state = ' '
                destroy_sub_screen()
                update = update + 100
                if isLoop.get():
                    # 等待任意键的输入
                    keyboard.read_key()
                    Thread(name='run in 退出养肝阶段', target=run, daemon=True).start()
                update_target()

        def check_window_position():
            #print('**check position start **')
            if force and now_state in fullStage:
                monitors = get_monitors()
                if v_["full_screen"] and v_["split_screen"]:
                    if len(monitors) != len(before_monitors):
                        destroy_sub_screen()
                        print('当前屏幕：', monitors)
                        print(f'增加多屏锁定2 屏幕数量不一致 before{len(before_monitors)} now:{len(monitors)}')
                        span()
                    else:
                        for m1, m2 in zip(monitors, before_monitors):
                            if m1.width != m2.width or m1.height != m2.height or m1.x != m2.x or m1.y != m2.y:
                                destroy_sub_screen()
                                span()
                                print('当前屏幕：', monitors)
                                print('增加多屏锁定3 屏幕位置变化')
                if v_["mouse_lock"]:
                    ui.moveTo(0, 0)
                    ui.click()
                window_x = root.winfo_x()
                window_y = root.winfo_y()
                if v_["full_screen"] and (window_x != 0 or window_y != 0):
                    root.attributes('-fullscreen', False)
                    root.attributes('-fullscreen', True)
                    print('错位重置')


        # 组件管理
        Thread(name='monitor', target=monitor, daemon=True).start()
        # dir=v_["block_website"]["proxy_rules_location"]\
        if v_["block_website"]["enable"]:
            block_website = BlockWebsite(block_websites=v_["block_website"]["websites"], dir=v_["block_website"]["proxy_rules_location"])
            Thread(name='网页阻止', target=block_website.start, daemon=True).start()
            print('代理服务器开启')



        def close():
            if force:
                return
            global destory
            destory = True
            if blackSheet:
                blackSheet.stop()
            time.sleep(1)
            destroy_sub_screen()
            try:
                root.destroy()
                print('主线程结束')
            except Exception as e:
                print('主线程关闭异常', e)
                print(traceback.print_exc())


        def quit_me():
            write_configs(write_all=False, first_read=False)
            close()


        root.protocol("WM_DELETE_WINDOW", quit_me)


        def start_study(click_start_discipline=True):
            global click_update
            click_update = click_start_discipline
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

                    Execute.now_execute.stop()
                    Thread(name='重置start_study', target=run, daemon=True).start()
            if not click_start_discipline:
                showinfo(
                    title='重置成功',
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

        reload_button = ttk.Button(frame, text="重置", command=lambda: start_study(click_start_discipline=False))
        reload_button.pack(side='left', padx=10)

        jump_button = ttk.Button(frame, text="绯红之王", command=lambda: Execute.now_execute.jump())
        jump_button.pack(side='left', padx=10)

        frame2 = tk.Frame(clock1)
        frame2.pack(pady=5)

        loop_button = ttk.Checkbutton(frame2, text="永无止尽",
                                      variable=isLoop)
        loop_button.pack(padx=10, side='left')

        count_round = ttk.Label(frame2, textvariable=cnt_round)
        count_round.pack(fill='x', expand=True, side='left', padx=10)

        root.mainloop()
    except Exception as e:
        print('未知异常', e)
        print(traceback.print_exc())
