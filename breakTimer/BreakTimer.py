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
