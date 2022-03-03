#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/21 8:39
# @Author  : 王志鹏
# @Site    : 
# @File    : d2.py
# @Software: PyCharm
from abc import ABCMeta, abstractmethod


# from d1 import *
# 抽象观察者
class Observer():
    __metaclass__ = ABCMeta  # 本类为抽象类

    def __init__(self, name, sub):
        self.__name = name
        self.__sub = sub
    # 更新状态
    @abstractmethod
    def Update(self):
        pass

class NBAObserver(Observer):
    def __init__(self, name, sub):
        self.name = name
        self.sub = sub

    def Update(self):
        print "%s,%s,关闭NBA直播,继续工作" % (self.sub.action, self.name)


# 股票观察者
class StockObserver2(Observer):
    def __init__(self, name, sub):
        self.name = name
        self.sub = sub

    def Update(self):
        print "%s,%s,关闭股票行情,继续工作" % (self.sub.action, self.name)


class Secretary2():
    def __init__(self):
        self.people = []
        self.action = ""

    def addPeople(self, people):
        self.people.append(people)

    def delPeople(self, people):
        del self.people[people]

    # 通知
    def Notify(self):
        for i, v in enumerate(self.people):
            v.Update()

    # 前台状态
    def SecretaryAction(self, actiom):
        self.action = actiom


if __name__ == '__main__':
    secretary2 = Secretary2()

    nbaobserver1 = NBAObserver("小N",secretary2)
    stockobserver2 = StockObserver2("小古",secretary2)
    secretary2.addPeople(nbaobserver1)
    secretary2.addPeople(stockobserver2)
    secretary2.SecretaryAction("胡汉三来了")
    secretary2.Notify()


    pass
