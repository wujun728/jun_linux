#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/25 15:49
# @Author  : 王志鹏
# @Site    : 
# @File    : d3.py
# @Software: PyCharm
""""""
"""
状态模式(State): 当一个对象的内在状态改变时允许改变其行为,这个对象看起来像是改变了类
主要解决:状态模式主要解决的是一个对象的状态转换条件的表达式过于复杂的情况.把转台的判断逻辑转移到标识不用状态的一系列类中(或者方法中),
可以吧复杂的判断逻辑简化,
注:如果这个判断逻辑很简单,那么就没有必要使用状态模式了!!!
"""

from abc import *
import collections  # 有序字典


class Context:
    def __init__(self):
        self.hour = 9
        self.curr = ConcreteStateA()

    @property
    def state(self):
        return self.state

    @state.setter
    def set_state(self, s):
        self.curr = s

    def Request(self):
        self.curr.Handel(self)


class State:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def Handel(self, context): pass


class ConcreteStateA(State):
    def Handel(self, context):
        print "这里是状态A"
        context.curr = ConcreteStateB()
        context.hour = 12


class ConcreteStateB(State):
    def Handel(self, context):
        print "这里是状态B"
        context.curr = ConcreteStateA()
        context.hour = 21


if __name__ == '__main__':
    context = Context()
    context.hour = 9
    context.Request()
    context.Request()
    context.Request()
    print context.hour
    # d1 = {}
    # d1 = collections.OrderedDict()  # 将普通字典转换为有序字典
    # d1['a'] = 'A'
    # d1['b'] = 'B'
    # d1['c'] = 'C'
    # d1['d'] = 'D'
    # for k, v in d1.items():
    #     # print k, v
    #     pass
    #
    # d2 = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}
    # for k, v in d2.items():
    #     print k, v
