#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/25 15:17
# @Author  : 王志鹏
# @Site    : 
# @File    : d1.py
# @Software: PyCharm

"""场景上午状态好,中午想睡觉,下午渐恢复,加班苦煎熬"""
"""面向过程的方式-方法版"""

class MyType:
    def __init__(self):
        self.type = []
        self.flag = False

    def main(self,time,WokerType=False):
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
    mytype = MyType()
    mytype.main(12)
