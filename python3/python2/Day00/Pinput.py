""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 15:51
# @Author  : iByte
import operator

hint = '''funtion:
            1   funtion 1
            2   funtion 2
            3   funtion 3

please input number:'''
if __name__ == '__main__':
    while True:
        option = input(hint)  # 获取IO输入的值
        if operator.le(option, "1"):
            print("you chose funtion 1")
        elif operator.le(option, "2"):
            print("you chose funtion 2")
        elif operator.le(option, "3"):
            print("you chose funtion 3")
        elif operator.le(option, "4"):
            print("quit !")
            break
        else:
            print("disabled input ,please try again....")
