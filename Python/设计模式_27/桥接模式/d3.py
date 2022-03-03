#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2019/1/6 11:15
# @Author  : 王志鹏
# @Site    : 
# @File    : d3.py
# @Software: PyCharm


"""
桥接模式 Bridge:
将抽象部分与他的实现部分分离,使他们都可以独立的变化
合成/聚合复用原则: 尽量使用合成/聚合,尽量不要使用继承
解释:
什么叫抽象与他的实现分离,并不是说,让抽象类与其派生类分离,因为这就没有任何意义.实现指的是抽象类和他的派生类用来实现自己的对象
理解:
    实现系统可能有多多角度分类,每一种分类都可能有变化,那么就把这种多角度分离出来让他们独立变化,减少他们之间的耦合

松耦合的程序
手机品牌下有N,M
手机软件下有通讯录,游戏
手机软件聚合手机品牌
"""
from abc import ABCMeta, abstractmethod


# 手机软件抽象类
class HandsetSoft(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self): pass


# 手机品牌抽象类
class HandsetBrand(object):
    __metaclass__ = ABCMeta

    def __init__(self, soft):
        self.soft = soft

    @abstractmethod
    def run(self): pass


class HandsetBreandN(HandsetBrand):
    def run(self):
        print "N牌手机"
        self.soft.run()


class HandsetBreandM(HandsetBrand):
    def run(self):
        print "M牌手机"
        self.soft.run()


class HandsetMP3(HandsetSoft):
    def run(self):
        print "运行手机MP3"


class playGame(HandsetSoft):
    def run(self):
        print "运行手机游戏"


class AddressList(HandsetSoft):
    def run(self):
        print "运行手机通讯录"


if __name__ == '__main__':
    # ab = HandsetBrand()
    ab = HandsetBreandN(HandsetMP3())
    ab.run()
    print "----------"
    ab = HandsetBreandM(AddressList())
    ab.run()

    # ab.set
