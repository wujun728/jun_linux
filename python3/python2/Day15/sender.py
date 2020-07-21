""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# coding: utf-8
from __future__ import unicode_literals
from threading import Timer
from wxpy import *

bot = Bot('bot.pkl')
my_friend = bot.friends().search("iByte")[0]


def send_message():
    try:
        my_friend.send(u"你到家了么！")
        t = Timer(86400, send_message)
        t.start()
    except:
        my_friend.send(u"今天消息发送失败了")


@bot.register(my_friend)
def reply_my_friend(msg):
    print(11)
    print(msg.text, msg.sender)


if __name__ == "__main__":
    send_message()
