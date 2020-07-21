""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/14 11:05
# @Author  : iByte


import time
import datetime

if __name__ == '__main__':

    nowtime = datetime.datetime.now()
    print(nowtime)
    strNowTime = nowtime.strftime("%Y-%m-%d %H:%M:%S") # 格式化时间，变为字符串
    print(strNowTime)
    # 时间计算
    # nowtime = nowtime + datetime.timedelta(seconds=1) # 秒
    # print(nowtime)
    nowTime = nowtime + datetime.timedelta(days=1)  # 天
    print(nowTime)

    print(nowTime.year)
