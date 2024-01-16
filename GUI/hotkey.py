import win32con
import ctypes.wintypes as wintypes
import  ctypes
import winerror
import time

# 注册全局热键
def register_hotkey():
    user32 = ctypes.windll.user32
    # win32con.MOD_ALT, win32con.MOD_SHIFT, ord('i')
    if not user32.RegisterHotKey(None, 1,  win32con.MOD_SHIFT, win32con.MOD_SHIFT):
        print("Unable to register hotkey")
        return
    print("Hotkey registered")

# 拦截热键触发事件
def handle_hotkey():
    try:
        msg = wintypes.MSG()
        print('msg is', msg)
        while True:
            if ctypes.windll.user32.GetMessageA(ctypes.byref(msg), 0, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    # 在这里处理热键触发事件，可以选择执行自定义操作或者阻止默认操作
                    print("Hotkey pressed")
                ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))
    except Exception as e:
        print("Error occurred:", e)

# 取消注册热键
def unregister_hotkey():
    user32 = ctypes.windll.user32
    if not user32.UnregisterHotKey(None, 1):
        print("Unable to unregister hotkey")

# 主程序入口
if __name__ == "__main__":
    register_hotkey()
    handle_hotkey()  # 这个函数会一直运行，需要在适当的时候退出
    # unregister_hotkey()
