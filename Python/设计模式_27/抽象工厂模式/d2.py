#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/21 14:16
# @Author  : 王志鹏
# @Site    : 
# @File    : d2.py
# @Software: PyCharm

# 抽象工厂模式（Abstract Factory Pattern）是围绕一个超级工厂创建其他工厂。
# 该超级工厂又称为其他工厂的工厂。这种类型的设计模式属于创建型模式，它提供了一种创建对象的最佳方式。
# 在抽象工厂模式中，接口是负责创建一个相关对象的工厂，不需要显式指定它们的类。每个生成的工厂都能按照工厂模式提供对象。
# 抽象版 优化1
from abc import *
from d1 import *

class IUser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def insertUser(self): pass

    @abstractmethod
    def GetUer(self): pass


class AccessUser(IUser):
    def __init__(self, user):
        self.user = user

    def insertUser(self):
        print "在Access中给User表中增加一个记录 name: %s id: %s " % (self.user.id, self.user.name)

    def GetUer(self):
        print "在Accessr得到User (name: %s id: %s)" % (self.user.id, self.user.name)


class SqlServerUser(IUser):
    def __init__(self, user):
        self.user = user

    def insertUser(self):
        print "在SqlServer中给User表中增加一个记录 name: %s id: %s " % (self.user.id, self.user.name)

    def GetUer(self):
        print "在SqlServer得到User (name: %s id: %s)" % (self.user.id, self.user.name)


class IFactory():
    __metaclass__ = ABCMeta

    @abstractmethod
    def CreatUser(self): pass


class AccessFactory(IFactory):
    def CreatUser(self,user):
        accessUser = AccessUser(user)
        return accessUser


class SqlServerFactory(IFactory):
    def CreatUser(self,user):
        sqlServerUser = SqlServerUser(user)
        return sqlServerUser


if __name__ == '__main__':
    user = User()
    user.name = "d2Name"
    user.id = 22
    iFactory = AccessFactory()
    iUser = iFactory.CreatUser(user)
    iUser.insertUser()