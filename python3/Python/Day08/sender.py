# coding: utf-8
from __future__ import unicode_literals
from wxpy import *
import sys

# 日志告警这里有三个参数 %{type} %{path} %{message}，可根据自己的日志自行配置参数
if len(sys.argv) == 4:
    bot = Bot('bot.pkl')
    # my_friend = bot.friends().search('小柒2012')[0]
    # my_friend.send('Hello WeChat!')
    # print(bot.groups())
    alarm_group = bot.groups().search('监控报警')[0]
    message = "项目名：{type}, 日志路径 {path}，详细信息 {message}".format(type=sys.argv[1], path=sys.argv[2], message=sys.argv[3])
    alarm_group.send(message)

