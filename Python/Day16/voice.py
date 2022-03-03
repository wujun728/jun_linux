# -*- coding: utf-8-*-
__author__ = "小柒"
__blog__ = "https://blog.52itstyle.vip/"
import pyttsx3
import win32com.client
from aip import AipSpeech
from play import wm_player

"""
pip3 install pypiwin32
pip3 install pyttsx3
https://blog.52itstyle.vip/
https://pyttsx3.readthedocs.io/en/latest/
"""


def say():
    engine = pyttsx3.init()
    # 音色
    voices = engine.getProperty('voices')
    # 语速
    rate = engine.getProperty('rate')
    # 音量
    volume = engine.getProperty('volume')
    for voice in voices:
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', rate + 50)
        engine.setProperty('volume', volume + 1.9)
        engine.say("小柒2012真帅")
    engine.runAndWait()


def win_say():
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak("你好，小姐姐，能加个微信吗？")


def txt_say():
    f = open("52itstyle.txt", encoding='UTF-8')
    line = f.readline()
    engine = pyttsx3.init()
    while line:
        line = f.readline()
        print(line, end='')
        engine.say(line)
    engine.runAndWait()
    f.close()


""" 你的百度 APPID AK SK
https://console.bce.baidu.com/ai/#/ai/speech/app/list       应用列表
http://ai.baidu.com/docs#/TTS-Online-Python-SDK/top         API
"""


def du_say():
    app_id = '208522'
    api_key = 'sYi4GIqdPrzC4K80IFvA29pD'
    secret_key = 'rhF5SHsEuUAz3cs3TgTpj4jllTn11gFG'
    client = AipSpeech(app_id, api_key, secret_key)
    text = "生当作人杰，死亦为鬼雄。至今思项羽，不肯过江东。"
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
    wm_player('auido.mp3')


if __name__ == '__main__':
    # win_say()
    # say()
    # txt_say()
    du_say()


