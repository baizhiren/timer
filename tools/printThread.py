import threading

def show_all_threads():
    for thread in threading.enumerate():
        print(thread.name, thread)



def show_current_thread():
    current_thread = threading.current_thread()
    print("当前线程标识符:", current_thread.ident)
    print("当前线程名称:", current_thread.name)

