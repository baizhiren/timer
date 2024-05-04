#1. 定时观察clash是否开启关闭 ok
#2. 定时检查代理是否正确开启7891端口
#3. 屏蔽网站 ok
import json
from typing import List, Dict


# 定义自己的过滤器和相关处理逻辑
from breakTimer.ModifyProxyOption import ModifyProxyOption

fix_domains = ['madou.club', 'e-hentai.org', 'exhentai.org']



# 将自定义处理器添加到mitmproxy插件中

from breakTimer.Component import Component

def is_clash_running(host='localhost', port=7890):
    """检测Clash代理是否运行"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
           # print("Clash代理正在运行。")
            return True
        except ConnectionError:
           # print("Clash代理未运行。")
            return False


from breakTimer.Awake import *

class BlockWebsite(Component):

    def __init__(self, block_websites:List[Dict[str, str]], dir=''):
        super().__init__(name='禁用网站', retry=True)
        self.block_process = None
        self.pre_clash_running = None
        self.websites = block_websites # 可以在外部改变
        self.pre_website = -1
        self.filtered_domains = -1
        self.dir = dir
        self.success = True
        self.modify_proxy_option = None

    def todo(self):
        import yaml
        import os
        next_website = []
        new_website_name = set()
        # 已有的是否过期
        if self.pre_website != -1:
            for website in self.pre_website:
                if not check_expire(website["time"]):
                    next_website.append(website)
                    new_website_name.add(website["name"])

        for website in self.websites:
            if "time" in website:
                if check(website["time"]) and website.get("enable", 1):
                   if self.pre_website == -1 or website not in self.pre_website:
                        next_website.append(website)
                        new_website_name.add(website["name"])

        path = 'temp.txt'
        if self.pre_website != next_website:
            self.pre_website = next_website
            if self.filtered_domains != new_website_name:
                self.filtered_domains = new_website_name
                with open(path, "w", encoding="utf-8") as temp_file:
                    # 父进程准备数据并写入临时文件
                    temp_file.write(json.dumps(list(new_website_name)))
                print(f'todo:阻止网站变化{self.filtered_domains}')

        key = 'rules'
        if os.path.isdir(self.dir):
            for root, dirs, files in os.walk(self.dir):
                for file in files:
                    filename = os.path.join(root, file)
                    if '.yml' in filename:
                        with open(filename, 'r', encoding='utf-8') as file:
                            data = yaml.safe_load(file)

                        flag = False
                        for website_name in fix_domains:
                            if key in data:
                                if f'DOMAIN-SUFFIX,{website_name},REJECT' not in data[key]:
                                    print(f'代理block{website_name}')
                                    flag = True
                                    data[key] = [f'DOMAIN-SUFFIX,{website_name},REJECT'] + data[key]
                            else:
                                break
                        if flag:
                            with open(filename, 'w') as file:
                                yaml.dump(data, file)
                                print(f'文件{filename}修改成功')

        clash_running = is_clash_running()
        if self.pre_clash_running == clash_running:
            return
        else:
            print(f'todo:clash打开状态变化{clash_running}')


        self.pre_clash_running = clash_running
        if self.block_process != None:
            self.block_process.stop()

        from tools import tool
        debug = tool.is_debug()
        if debug:
            path = '../breakTimer/VPNForwarder.py'
        else:
            path = './_internal/source/VPNForwarder.py'

        if clash_running:
            # Clash正在运行，设置mitmproxy为upstream模式
            options = [
                '--mode', 'upstream:http://localhost:7890',  # 设置上游代理模式
                '-p', '7891',  # 指定监听端口
                '-s', path,  # 加载当前脚本作为addon
                '--set', 'connection_timeout=60',
                '--set', 'stream_large_bodies=100'
            ]
        else:
            # Clash未运行，设置mitmproxy为正常（regular）模式
            options = [
                '--mode', 'regular',  # 设置普通代理模式
                '-p', '7891',  # 指定监听端口
                '-s', path ,  # 加载当前脚本作为addon
                '--set', 'connection_timeout=60',
                '--set', 'stream_large_bodies=100'
            ]

        sys.argv = [sys.argv[0]] + options  # 重构命令行参数以模拟命令行输入

        mitm_thread = MitmDumpThread(sys.argv)
        mitm_thread.start()
        self.block_process = mitm_thread

        time.sleep(0.5)
        if mitm_thread.success:
            mp = ModifyProxyOption()
            threading.Thread(name='代理开关修改', target=mp.start, daemon=True).start()
            self.modify_proxy_option = mp

    def error(self):
        if self.modify_proxy_option:
            self.modify_proxy_option.stop()

    def stop(self):
        super().stop()
        if self.modify_proxy_option:
            self.modify_proxy_option.stop()
        self.block_process.stop()




import socket
from mitmproxy.tools.main import mitmdump
import sys



import subprocess
import threading
import time

class MitmDumpThread(threading.Thread):
    def __init__(self, argv):
        super().__init__()
        self.process = None  # 用来保留 subprocess.Popen 对象
        self.argv = argv
        self.success = True

    def run(self):
        import os

        # 替换为你要检查的文件的路径
        file_path = os.environ['USERPROFILE'] + "/.mitmproxy/mitmproxy-ca-cert.cer"

        if os.path.exists(file_path):
            print(f"mitmproxy 证书文件 {file_path} 存在。")
        else:
            print(f"mitmproxy 证书文件 {file_path} 不存在。")
            self.success = False
            return

        logfile = open('mitmproxy.log', 'w')
        # 使用 subprocess 启动 mitmdump
        #self.process = subprocess.Popen(['mitmdump', '--mode', 'regular'])
        print('argv is ', ['mitmdump'] + self.argv[1:])

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        self.process = subprocess.Popen(['mitmdump'] + self.argv[1:], stdout = logfile, stderr = logfile,  startupinfo=startupinfo)
        self.process.wait()  # 等待进程结束
        self.success = False
        print('mitmproxy进程结束')

    def stop(self):
        if self.process:
            self.process.terminate()  # 发送终止信号
            self.process.wait()  # 等待进程实际结束

# 创建并启动线程

#
# from tools.tool import is_debug
#
# if is_debug():
#     if __name__ == '__main__':
#         map = {
#             "enable": 1,
#             "proxy_rules_location": "C:\\Users\\chao/config/clash/profiles",
#             "websites": [
#                 {
#                     "name": "zhihu.com",
#                     "time": {
#                         "mode": "period",
#                         "interval": "2024.2.24 10:00-2024.2.24 11:30"
#                     }
#                 }
#             ]
#         }
#
#         bw = BlockWebsite(block_websites=map["websites"])
#         bw.start()
#     #     # time.sleep(5)
#     #     # print('20s 已到， 今日起兵！')
#     #     # map["websites"] = [
#     #     #     {
#     #     #         "name": "bilibili.com",
#     #     #         "time": {
#     #     #             "mode": "period",
#     #     #             "interval": "2024.2.22 10:00-2024.2.22 11:26"
#     #     #         }
#     #     #     }
#     #     #
#     #     # ]
#     #     # bw.websites = map["websites"]
#         time.sleep(100000)