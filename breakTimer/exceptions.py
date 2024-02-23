custom_exception = type("para Error", (Exception,), {"__str__": lambda self: "用户参数错误"})

def my_exception(name:str):
    return type("para Error", (Exception,), {"__str__": lambda self: f'{name}'})
