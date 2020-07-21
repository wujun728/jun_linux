#!/usr/bin/env python
# -*- coding: utf-8 -*-  
'''
@author: xiaoshui
@contact: opsonly.com@gmail.com
@file: urls.py
@time: 2018/12/6 16:06
@desc:
'''
from django.urls import path
from . import views
app_name = 'remark'

urlpatterns = [
    path('remark/<int:id>/',views.remark,name='remark'),
    path('reply/<int:id>/<int:aid>',views.reply,name='reply'),
    path('commit/<int:id>/<int:aid>',views.commit,name='commit'),

]