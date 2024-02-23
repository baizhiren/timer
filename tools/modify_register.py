import winreg


def modify(name, subkey, type, value, key=winreg.HKEY_CURRENT_USER):
    access = winreg.KEY_WRITE
    reg = winreg.ConnectRegistry(None, key)
    key = winreg.OpenKey(reg, subkey, 0, access)
    # 修改代理服务器地址和端口
    winreg.SetValueEx(key, name, 0, type, value)  # 启用代理
    # 关闭注册表
    winreg.CloseKey(key)

def read(subkey, name, key=winreg.HKEY_CURRENT_USER):
    reg = winreg.OpenKey(key,subkey, 0, winreg.KEY_READ)
    value, value_type = winreg.QueryValueEx(reg, name)
    return value, value_type