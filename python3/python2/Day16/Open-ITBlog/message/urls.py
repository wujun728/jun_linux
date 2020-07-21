#!/usr/bin/env python
# -*- coding: utf-8 -*-  
'''
@author: xiaoshui
@contact: opsonly.com@gmail.com
@file: urls.py
@time: 2018/12/5 16:32
@desc:
'''

from django.urls import path
from . import views
app_name = 'message'

urlpatterns = [
    path('reply/<int:id>/',views.reply,name='reply'),
    path('commit/<int:id>/',views.commit,name='commit'),
    path('message/',views.get_message,name='message'),
    path('message-list/',views.message_list,name='message_list'),
]