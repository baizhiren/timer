#已废弃

import time

from breakTimer.Component import Component
from breakTimer.BlackSheet import BlackSheet


import yaml
import os


class ModifyMonitor(Component):
    def __init__(self, time_gap=10, dir='C://Users//chao//.config//clash//profiles',
                 proxy_block_websites=[]):
        super().__init__(time_gap=time_gap, name='代理检测')
        self.proxy_block_websites = proxy_block_websites
        self.dir = dir

    def todo(self):

        # from tools.printThread import show_current_thread
        # print('in todo_')
        # show_current_thread()
        key = 'rules'
        if os.path.isdir(self.dir):
            for root, dirs, files in os.walk(self.dir):
                for file in files:
                    filename = os.path.join(root, file)
                    if '.yml' in filename:
                        with open(filename, 'r', encoding='utf-8') as file:
                            data = yaml.safe_load(file)

                        flag = False
                        for website_name in website_names:
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
                                #BlackSheet(list=["msedge.exe","chrome.exe"]).todo()
                                #print('关闭浏览器')
# 不可以
# if __name__ == '__main__':
#     m = ModifyMonitor()
#     m.start()
#     time.sleep(10000)
