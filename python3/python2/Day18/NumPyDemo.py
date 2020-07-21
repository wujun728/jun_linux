""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/6 11:17
# @Author  : iByte
import numpy as np


"""
以下实例获取数组中(0,0)，(1,1)和(2,0)位置处的元素。
"""


def numpy_demo():
    x = np.array([[1, 2], [3, 4], [5, 6]])
    y = x[[0, 1, 2], [0, 1, 0]]
    print(y)


if __name__ == '__main__':
    numpy_demo()
    np.empty()
