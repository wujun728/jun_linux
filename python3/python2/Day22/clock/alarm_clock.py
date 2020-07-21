""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/11 19:19
# @Author  : iByte

import time
import random
import os
import pygame
import urllib.request
import json
from aip import AipSpeech

"""
iByte 打造智能闹钟
pip3 install pygame
pip3 install baidu-aip
"""

# 获取天气
def get_weather():
    # 深圳天气
    url = 'http://www.weather.com.cn/data/cityinfo/101090108.html'
    obj = urllib.request.urlopen(url)
    data_b = obj.read()
    data_s = data_b.decode('utf-8')
    data_dict = json.loads(data_s)
    rt = data_dict['weatherinfo']
    weather = '亲爱的：该起床了，别睡了，快变小猪了，哈哈哈哈哈，我想你了，你想我吗？深圳的温度是 {} 到 {}，天气 {}'
    weather = weather.format(rt['temp1'], rt['temp2'], rt['weather'])
    if '雨' in weather:
        weather += '今天别忘记带雨伞哦！'
    du_say(weather)


# 文字转语音
def du_say(weather):
    app_id = '208522'
    api_key = 'sYi4GIqdPrzC4K80IFvA29pD'
    secret_key = 'rhF5SHsEuUAz3cs3TgTpj4jllTn11gFG'
    client = AipSpeech(app_id, api_key, secret_key)
    # per 3是汉子 4是妹子
    result = client.synthesis(weather, 'zh', 1, {
        'vol': 5, 'per': 3, 'spd': 3
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('weather.mp3', 'wb') as f:
            f.write(result)
    py_game_player('weather.mp3')


# 播放天气和音乐
def py_game_player(file):
    pygame.mixer.init()
    print("播报天气")
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=1, start=0.0)
    print("播放音乐")
    while True:
        if pygame.mixer.music.get_busy() == 0:
            # Linux 配置定时任务要设置绝对路径
            # mp3 = "/home/pi/alarmClock/"+str(random.randint(1, 6)) + ".mp3"
            mp3 = str(random.randint(1, 6)) + ".mp3"
            pygame.mixer.music.load(mp3)
            pygame.mixer.music.play(loops=1, start=0.0)
            break
    while True:
        if pygame.mixer.music.get_busy() == 0:
            print("起床啦")
            break


if __name__ == '__main__':
    get_weather()




