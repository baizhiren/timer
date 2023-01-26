# -*- coding:utf-8 -*-
import time
import datetime
from functools import partial
from threading import Timer, Thread

from breakTimer.SystemMusic import SystemMusic


class BreakTimer:
    # 单位：分钟
    smallTime = 5
    bigTime = 30
    studyTime = 45
    smallNum = 1

    def __init__(self, smallTime=5, bigTime=45, studyTime=45, smallNum=1, **kw):
        self.small_num = smallNum
        self.smallTime = smallTime
        self.studyTime = studyTime
        self.bigTime = bigTime

        for k, v in kw:
            self.k = v

    def start(self):
        # now = time.localtime(time.time())
        # date = datetime.datetime(now[0], now[1], now[2], now[3], now[4], now[5])
        # timeTable = []
        # for i in range(self.smallNum):
        #     self.timeTable.append(date + datetime.timedelta(minutes=self.studyTime))
        #     self.timeTable.append(date + datetime.timedelta(minutes=self.smallTime))
        # self.timeTable.append(date + datetime.timedelta(minutes=self.bigTime))
        music = SystemMusic()
        st = 0
        for i in range(self.smallNum):
            st += self.studyTime
            Timer(st * 60, partial(music.ring, id=0)).start()
            st += self.smallTime
            Timer(st * 60, partial(music.ring, id=0)).start()

        st += self.studyTime
        Timer(st * 60, partial(music.ring, id=0)).start()
        st += self.bigTime
        Timer(st * 60, partial(music.ring, id=0)).start()
