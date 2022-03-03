#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/25 15:36
# @Author  : 王志鹏
# @Site    : 
# @File    : d2.py
# @Software: PyCharm
"""分类版"""
"""
1.方法过长坏味道! 违反单一职责,有很多判断责任太大了!
2.假如:要求所有人必须在二十点之前离开公司改动风险很大,违反开放-封闭原则
"""


class Woker:
    def __init__(self, times, WokerType):
        self.__times = times
        self.__WokerType = WokerType

    def WriteProgram(self):
        def main(self, time, WokerType=False):
            if time < 12:
                print "当前时间{%s}点,上午工作,精神百倍" % time
            elif time < 13:
                print "当前时间{%s}点,饿了,午饭,犯困,午休." % time
            elif time < 17:
                print "当前时间{%s}点,饿了,下午状态还不错,继续努力." % time
            else:
                if WokerType:
                    print "当前时间{%s}点,下班回家." % time
                else:
                    if time < 21:
                        print "当前时间{%s}点,加班中.非常疲劳" % time
                    else:
                        print "当前时间{%s}点,完蛋了,睡着了!!" % time


if __name__ == '__main__':
    pass
