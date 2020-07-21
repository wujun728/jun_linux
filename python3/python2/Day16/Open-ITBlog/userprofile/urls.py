#!/usr/bin/env python
# -*- coding: utf-8 -*-  
'''
@author: xiaoshui
@contact: opsonly.com@gmail.com
@file: urls.py
@time: 2018/11/20 11:34
@desc:
'''
from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    path('delete/<int:id>/',views.user_delete,name='delete'),

]