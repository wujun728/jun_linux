#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/25 16:56
# @Author  : 王志鹏
# @Site    : 
# @File    : cp4.py
# @Software: PyCharm

# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""
大话设计模式
设计模式——状态模式
状态模式(State Pattern):当一个对象的内在状态改变时允许改变其行为，这个对象看起来像是改变了其类
应用场景:当控制一个对象的状态转换的条件表达式过于复杂时,把状态的判断逻辑转移到表示不同状态的一系列类当中,可以把复杂的判断逻辑简化
(当一个对象的行为取决于它的状态,并且它必须在运行时刻根据状态改变他的行为)
"""


class State(object):
    def __init__(self):
        pass

    def write_program(self, w):
        pass


class Work(object):
    def __init__(self):
        self.hour = 9
        self.curr = ForenoonState()

    def set_state(self, s):
        self.curr = s

    def write_program(self):
        self.curr.write_program(self)


class ForenoonState(State):
    def write_program(self, w):
        if w.hour < 12:
            print "当前时间:%s点," % w.hour, "精神百倍"
        else:
            w.set_state(AfternoonState())
            w.write_program()


class AfternoonState(State):
    def write_program(self, w):
        if w.hour < 17:
            print "当前时间:%s点," % w.hour, "状态还行,继续努力"
        else:
            w.set_state(EveningState())
            w.write_program()


class EveningState(State):
    def write_program(self, w):
        if w.hour < 21:
            print "当前时间:%s点," % w.hour, "加班呢,疲劳了"
        else:
            w.set_state(SleepState())
            w.write_program()


class SleepState(State):
    def write_program(self, w):
        print "当前时间:%s点," % w.hour, "不行了,睡着了"


if __name__ == "__main__":
    work = Work()
    work.hour = 9
    work.write_program()

    # work.hour = 15
    # work.write_program()
    # work.hour = 20
    # work.write_program()
    # work.hour = 22
    # work.write_program()
