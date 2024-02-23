#1. 定时观察clash是否开启关闭 ok
#2. 定时检查代理是否正确开启7891端口
#3. 屏蔽网站 ok
import json
import os
from typing import List, Dict

import yaml
from mitmproxy import http
from mitmproxy import ctx
# 定义自己的过滤器和相关处理逻辑

class VPNForwarder:

    def request(self, flow):
        with open('temp.txt', 'r') as file:
            filtered_domains = json.load(file)
        filtered_domains = list(set(filtered_domains + fix_domains))

        ctx.log.info(f'{ctx}')
        # ctx.log.info(f'当前阻止网站: {filtered_domains}')
        # 对特定域名请求不进行转发
        response_body = "滚去学习".encode('utf-8')  # 使用 utf-8 编码
        if any(domain in flow.request.pretty_host for domain in filtered_domains):
            ctx.log.info(f'成功阻止网站:{filtered_domains}')

        #     flow.response = http.HTTPResponse.make(
        #         403,
        #         #b'forbidden, go to study, be a person',
        #         response_body,
        #         {"Content-Type": "text/html; charset=utf-8"}
        # )
            flow.response = http.Response.make(
                403,  # 状态码
                #b"forbidden, go to study, be a person",  # 响应体
                response_body,
                {"Content-Type": "text/html; charset=utf-8"}  # 头部
            )
        # 其他请求会自动通过上游代理，无需在这里指定

addons = [
    VPNForwarder()
]



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


from breakTimer.Awake import  check

class BlockWebsite(Component):
    def __init__(self, block_websites:List[Dict[str, str]], dir='C://Users//chao//.config//clash//profiles'):
        super().__init__(name='禁用网站')
        self.block_process = None
        self.pre_clash_running = None
        self.websites = block_websites
        self.filtered_domains = []
        self.dir = dir

    def todo(self):
        websites_names = []
        for website in self.websites:
            if "time" in website:
                if check(website["time"]):
                    websites_names.append(website["name"])

        #
        path = 'temp.txt'
        if websites_names != self.filtered_domains:
            self.filtered_domains = websites_names
            with open(path, "w", encoding="utf-8") as temp_file:
                # 父进程准备数据并写入临时文件
                temp_file.write(json.dumps(websites_names))
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
            path = __file__
        else:
            path = './_internal/BlockWebsite.py'


        if clash_running:
            # Clash正在运行，设置mitmproxy为upstream模式
            options = [
                '--mode', 'upstream:http://localhost:7890',  # 设置上游代理模式
                '-p', '7891',  # 指定监听端口
                '-s', path,  # 加载当前脚本作为addon
                '--set', 'connection_timeout=60',
                '--set', 'stream_large_bodies=3k',

            ]
        else:
            # Clash未运行，设置mitmproxy为正常（regular）模式
            options = [
                '--mode', 'regular',  # 设置普通代理模式
                '-p', '7891',  # 指定监听端口
                '-s', path,  # 加载当前脚本作为addon
                '--set', 'connection_timeout=60',
                '--set', 'stream_large_bodies=3k',
            ]

        # 根据需求可能还需要其他参数
        # '-s', 'path_to_your_script.py',  # 加载当前脚本作为addon等

        sys.argv = [sys.argv[0]] + options  # 重构命令行参数以模拟命令行输入

        mitm_thread = MitmDumpThread(sys.argv)
        mitm_thread.start()
        self.block_process = mitm_thread




import socket
from mitmproxy.tools.main import mitmdump
import sys

fix_domains = ['madou.club', 'e-hentai.org', 'exhentai.org']

import subprocess
import threading
import time

class MitmDumpThread(threading.Thread):
    def __init__(self, argv):
        super().__init__()
        self.process = None  # 用来保留 subprocess.Popen 对象
        self.argv = argv

    def run(self):
        logfile = open('mitmproxy.log', 'w')
        # 使用 subprocess 启动 mitmdump
        #self.process = subprocess.Popen(['mitmdump', '--mode', 'regular'])
        print('argv is ', ['mitmdump'] + self.argv[1:])
        self.process = subprocess.Popen(['mitmdump'] + self.argv[1:], stdout = logfile, stderr = logfile)
        self.process.wait()  # 等待进程结束

    def stop(self):
        if self.process:
            self.process.terminate()  # 发送终止信号
            self.process.wait()  # 等待进程实际结束

# 创建并启动线程



# if __name__ == '__main__':
#     path =
#     with open(path, "r") as file:
    # map = {
    #     "enable": 1,
    #     "proxy_rules_location": "C:\\Users\\chao/config/clash/profiles",
    #     "websites": [
    #         {
    #             "name": "zhihu.com",
    #             "time": {
    #                 "mode": "day",
    #                 "interval": "00:00-8:40"
    #             }
    #         }
    #     ]
    # }
    # bw = BlockWebsite(block_websites=map["websites"])
    # bw.start()
    # time.sleep(100000)