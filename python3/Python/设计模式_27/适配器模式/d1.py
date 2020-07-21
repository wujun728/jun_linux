#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/12/28 13:43
# @Author  : 王志鹏
# @Site    : 
# @File    : d1.py
# @Software: PyCharm.
"""
适配器模式 Adapter, 将一个类的接口转换成客户希望的另外一个接口.
Adapter 模式使原本由于接口不兼容而不能一起工作的那些类可以一起工作DP
"""


class Target(object):
    def Request(self):
        print "普通请求"


class Adaptee(object):
    def specificRequest(self):
        print "特殊请求"

class Adapter(Adaptee):
    def __init__(self):
        self.adaptee = Adaptee()
    def Request(self):
        self.adaptee.specificRequest()

if __name__ == '__main__':
    """模拟客户端代码"""
    target = Adapter()
    target.Request()