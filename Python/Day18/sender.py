# coding: utf-8
from __future__ import unicode_literals
import requests
import urllib3
import json
from threading import Timer
from wxpy import *

bot = Bot('bot.pkl')


def xiaohuangji(content):
    url = r'http://www.tuling123.com/openapi/api?key=77aa5b955fcab122b096f2c2dd8434c8&info='+content  #请求的网址
    reson = urllib3.urlopen(url)
    reson = json.loads(reson.read())
    return reson['text'].encode('utf-8')


def get_message():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    contents = r.json()['content']
    translation = r.json()['translation']
    return contents, translation


def send_message():
    try:
        my_friend = bot.groups().search('爪哇笔记')[0]
        my_friend.send(get_message()[0])
        my_friend.send(get_message()[1][5:])
        my_friend.send(u"来自爪哇笔记的心灵鸡汤！")
        t = Timer(86400, send_message)
        t.start()
    except:
        my_friend = bot.friends().search('宋晖0120')[0]
        my_friend.send(u"今天消息发送失败了")


if __name__ == "__main__":
    send_message()

