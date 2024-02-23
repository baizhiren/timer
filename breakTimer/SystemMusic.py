import threading
import time
import winsound
from playsound import playsound


from pycaw.pycaw import AudioUtilities
import pyautogui


class SystemMusic:
    duration = 1000  # 持续时间/ms
    frequency = 500  # 频率/Hz
    cancel_tmr = False
    time_gap = 3
    from tools.tool import is_debug
    if not is_debug():
        song = ['_internal/source/shine.wav']
    else:
        song = ['D:/work/python_code/protect/source/shine.wav']

    def __init__(self, **kw):
        for k, v in kw:
            self.k = v

    def ring(self, time_gap=3, n=2, id=0):
        if id == -1:
            self.time_gap = time_gap
            self.heart_beat()
            time.sleep(time_gap * n)
            self.cancel_tmr = True
            time.sleep(5)
            self.cancel_tmr = False
        else:
            for i in range(n):
                playsound(self.song[id])

    def beep(self):
        winsound.Beep(self.frequency, self.duration)

    def heart_beat(self):
        # 打印当前时间
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        if not self.cancel_tmr:
            threading.Timer(0, self.beep).start()
            threading.Timer(self.time_gap, self.heart_beat).start()

    @staticmethod
    def is_audio_playing():
        import pythoncom
        # 在需要初始化COM库的地方调用CoInitialize函数
        pythoncom.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session.SimpleAudioVolume
            if volume.GetMute() == 0 and volume.GetMasterVolume() > 0:
                # 检查音频会话是否有声音输出（会话的状态为音频播放）
                if session.State == 1:  # 1代表会话处于活动状态
                    print(f"声音正在播放：{session.DisplayName}")
                    return True
        return False

    @staticmethod
    def simulate_media_play_pause():
        # 模拟媒体播放/暂停按键
        # 注意: VK_MEDIA_PLAY_PAUSE的虚拟键码为179
        pyautogui.press('playpause')

    @staticmethod
    def pause():
        # 模拟媒体播放/暂停按键
        # 注意: VK_MEDIA_PLAY_PAUSE的虚拟键码为179
        if SystemMusic.is_audio_playing():
            SystemMusic.simulate_media_play_pause()
            print('***暂停播放')
        else:
            print("音频没有播放")



# if __name__ == '__main__':
#     # winsound.Beep(1000, 1000)
#     # music = SystemMusic()
#     # music.ring(id=0)
#     SystemMusic.pause()

