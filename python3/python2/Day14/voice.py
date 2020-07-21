""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# -*- coding: utf-8-*-
import pyttsx3
import win32com.client
from aip import AipSpeech
from playsound import playsound

"""
下载依赖包
pip3 install pypiwin32
pip3 install pyttsx3
pip3 install baidu-aip
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
        engine.say("李尚志真帅")
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
    app_id = '16345921'
    api_key = 'ketbkfKRYP3L6j8GlGV2P5Ga'
    secret_key = 'Ilb4PwCvCa5Fusf5YkuASMKEDUbvSGBe'
    client = AipSpeech(app_id, api_key, secret_key)
    text = "小伙子，脚好点了没？严重不严重？"
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
        'per': 3,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
    playsound('auido.mp3')


if __name__ == '__main__':
    #win_say()
     say()
    #txt_say()
    #du_say()


