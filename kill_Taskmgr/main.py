from threading import Thread, Timer
import psutil


def check():
    list = ['Taskmgr.exe']
    for proc in psutil.process_iter(['pid', 'name']):
        for process_name in list:
            if process_name.lower() == proc.info['name'].lower():
                print(f'黑名单杀掉{proc.info["name"]}')
                try:
                    pid = proc.info['pid']
                    p = psutil.Process(pid)
                    p.terminate()
                except Exception as e:
                    print(e)
                    print('关闭', proc, '错误')
    Timer(1, check).start()

if __name__ == '__main__':
    check()
    print('hello')