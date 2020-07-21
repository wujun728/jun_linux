#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/21 9:35
# @Author  : 王志鹏
# @Site    : 
# @File    : d3.py
# @Software: PyCharm

# 双向解耦 抽象观察者,抽象通知者
from abc import ABCMeta, abstractmethod
# 通知者接口
class Subject3():
    __metaclass__ = ABCMeta
    def __init__(self):
        self.peopleList = []
        self.subjectStatce = ""
    @abstractmethod
    def addPeople(self):
        pass
    @abstractmethod
    def delPeople(self):
        pass
    # 通知
    @abstractmethod
    def Notify(self):
        pass
    # 通知状态
    @abstractmethod
    def subjecStatce(self):
        pass
# 观察者接口
class Obsevice3():
    __metaclass__ = ABCMeta

    def __init__(self, name, sub):
        self.name = name
        self.sub = sub

    @abstractmethod
    def Update(self):
        pass

# 股票观察者
class stickObserver3(Obsevice3):
    def Update(self):#AAA
        print "%s,%s,关闭股票行情,继续工作" % (self.sub.subjectStatce, self.name)

class NBAObserver3(Obsevice3):
    def Update(self):#BBB
        print "%s,%s,关闭NBA直播,继续工作" % (self.sub.subjectStatce, self.name)

class Boss3(Subject3):

    def addPeople(self, people):
        self.peopleList.append(people)

    def delPeople(self, people):
        self.delPeople(people)

    def Notify(self):
        for i, v in enumerate(self.peopleList):
            v.Update()

    def subjecStatce(self, subjectStatce):
        self.subjectStatce = subjectStatce

if __name__ == '__main__':
    # 通知者
    Boss3 = Boss3()

    # 看股票的同事
    stockobserver1 = stickObserver3("小王", Boss3)
    nbaobserver2 = NBAObserver3("小N", Boss3)

    Boss3.addPeople(stockobserver1)
    Boss3.addPeople(nbaobserver2)

    # 发现老板回来改变状态
    Boss3.subjecStatce("我胡汉三来了!!!")
    # 通知人员
    Boss3.Notify()