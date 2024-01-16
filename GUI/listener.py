import pyHook
import pythoncom

# 拦截键盘事件
def OnKeyboardEvent(event):
    if event.Alt and event.Shift and event.Key == "Left":
        # 在这里处理拦截到的 Win + Shift + 左箭头事件
        print("Win + Shift + Left intercepted")
        return False  # 返回 False 表示拦截该事件
    return True

# 创建钩子管理器
hm = pyHook.HookManager()
# 监听键盘事件
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

# 开始消息循环
pythoncom.PumpMessages()