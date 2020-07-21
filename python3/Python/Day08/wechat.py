# coding: utf-8
from __future__ import unicode_literals
from wxpy import *
from wechat_sender import listen
bot = Bot('bot.pkl')
listen(bot)


