__author__ = "小柒"
__blog__ = "https://blog.52itstyle.vip/"
import time
import os
import pygame

"""
播放音频文件
pip3 install pygame
https://blog.52itstyle.vip/
https://www.pygame.org/contribute.html
"""


def wm_player(mp3):
    os.system(mp3)
    time.sleep(10)
    os.system("taskkill /F /IM wmplayer.exe")


def py_game_player():
    file = r'649551350.mp3'
    pygame.mixer.init()
    print("播放音乐")
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    time.sleep(1000)
    pygame.mixer.music.stop()


if __name__ == '__main__':
    py_game_player("649551350.mp3")

