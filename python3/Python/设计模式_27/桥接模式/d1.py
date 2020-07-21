#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2019/1/6 9:32
# @Author  : 王志鹏
# @Site    : 
# @File    : d1.py
# @Software: PyCharm


# 紧耦合的程序演化
# 1.如果现在有一个N品牌的手机,它有一个小游戏,我要玩游戏
# 2.增加M品牌的手机,也玩游戏
# 3.增加通讯录功能
from abc import ABCMeta, abstractmethod


class Game(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def playGame(selfe): pass


class Nphone(Game):
    def playGame(self):
        print "N--玩游戏!"

class Mphone(Game):
    def playGame(self):
        print "M--玩游戏!"

if __name__ == '__main__':
    nphone = Nphone()
    nphone.playGame()

    mphone = Mphone()
    mphone.playGame()