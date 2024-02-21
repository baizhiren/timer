import time
import winreg

from breakTimer.Component import Component
from tools.modify_register import modify, read
class ModifyProxyOption(Component):
    def __init__(self, port=7891):
        super().__init__(name='修改代理选项', time_gap=2)
        self.block_process = None
        self.pre_clash_running = None
        self.port = port
    def todo(self):
        modify("ProxyServer", r'SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings', winreg.REG_SZ, f'127.0.0.1:{self.port}')
        modify("ProxyEnable", r'SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings', winreg.REG_DWORD, 1)

# if __name__ == '__main__':
#     mpo = ModifyProxyOption()
#     mpo.start()
#     time.sleep(100000)