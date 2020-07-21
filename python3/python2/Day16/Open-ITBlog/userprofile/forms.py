#!/usr/bin/env python
# -*- coding: utf-8 -*-  
'''
@author: xiaoshui
@contact: opsonly.com@gmail.com
@file: forms.py
@time: 2018/11/20 10:21
@desc:
'''

from django import  forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    # 确认输入的密码
    password = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username','email')

    def clean_password2(selfd):
        data = selfd.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重新输入")