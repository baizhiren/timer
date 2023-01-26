# SuperFastPython.com
# example of a thread executing a custom function
from functools import partial
from multiprocessing import Process
import time
from threading import Thread, Timer

def say():
    print("this is sya!!")



# custom task function
def task(id):
    #Timer(4, say)
    print(id)
    # execute a task in a loop
    for i in range(5):
        # block for a moment
        time.sleep(1)
        # report a message
        print('Worker thread running...')
    print('Worker closing down')


# # create and configure a new thread
# thread = Thread(target=task)
# # start the new thread
# thread.start()
# # wait for the new thread to finish
#
# thread.join()
# print("the end")
if __name__ == '__main__':
    p = Process(target=partial(task, id=10))
    p.start()

    time.sleep(3)

    p.terminate()
    print('is all over')
