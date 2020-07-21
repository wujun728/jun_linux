# coding: utf-8
from __future__ import unicode_literals

from wxpy import *
from wechat_sender import listen

"""
升级：pip install --upgrade pip
安装模块：pip install wechat_sender
"""

bot = Bot('bot.pkl')
listen(bot)

