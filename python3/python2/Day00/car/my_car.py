""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/14 11:37
# @Author  : iByte
from Day00.car.car import Car

if __name__ == '__main__':
    my_new_car = Car('audi', 'a8', 2018)
    print(my_new_car.get_descriptive_name())

    my_new_car.odometer_reading = 23
    my_new_car.read_odometer()
