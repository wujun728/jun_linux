#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/21 13:20
# @Author  : 王志鹏
# @Site    : 
# @File    : d1.py
# @Software: PyCharm

# 场景换需求更换或者选择 DB方式

"""
提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类
优点：易于交换“产品系列”，只要更改相应的工厂即可。
缺点：建立产品的时候很繁琐，需要增加和修改很多东西。

优化1：为了避免客户端有过多的逻辑判断，可以封装出一个简单工厂类来生成产品类。
优化2：为了减少简单工厂类里面的逻辑判断，可以采用“反射”机制，直接根据外部的配置文件读取出需要使用产品类的信息。

"""

from abc import ABCMeta, abstractmethod


class User():
    def __init__(self):
        self.name = None
        self.id = None

    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, id):
        if isinstance(id, str):
            self.id = int(id)
        elif isinstance(id, int):
            self.id = id

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.name = int(name)


class SqlServerUser():
    def __init__(self, user):
        self.user = user

    def insertUser(self):
        print "在SqlServer中给User表中增加一个记录 name: %s id: %s " % (self.user.id, self.user.name)

    def GetUer(self):
        print "在SqlServer得到User (name: %s id: %s)" % (self.user.id, self.user.name)


class IUser:
    __metaclass__ = ABCMeta

    def insertUser(self): pass

    def GetUer(self): pass


if __name__ == '__main__':
    pass
    user = User()
    user.name = "小王"
    user.id = 11
    # print user.id
    # print user.name
    sqlserveruser = SqlServerUser(user)
    sqlserveruser.insertUser()
    sqlserveruser.GetUser()
