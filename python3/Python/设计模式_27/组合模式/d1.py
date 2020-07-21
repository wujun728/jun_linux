#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/12/30 15:18
# @Author  : 王志鹏
# @Site    : 
# @File    : d1.py
# @Software: PyCharm

"""
组合模式 Composite , 将对象组组合成树形结构以表示'部分-整体' 的层次结构.组合模式使得用户对单个对象的组合对象的使用具有一致性
"""

from abc import ABCMeta, abstractmethod


# 组合的对象声明接口,在适当情况下,实现所有类共有接口的默认行为,声明一个接口用于访问和管理Component的子部件
class Compoente(object):
    pass
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    def Add(self, c): pass

    def Remove(self, c): pass

    def Display(self, deph): pass


# 在组合中表示叶节点对象叶节点没有子节点
class Leaf(Compoente):
    pass

    # def __init__(self, name):
    #     self.name = self.name

    def Add(self, c):
        print "不能添加下级节点"

    def Remove(self, c):
        print "不能删除下级节点"

    def Display(self, deph):
        pass
        strTemp = ""
        for i in range(deph):
            strTemp += strTemp + "-"
        print deph, self.name


# 定义有枝节点的行为,用来储存子部件有关操作比如增加Add和Remove
class Composite(Compoente):
    pass

    def __init__(self, name):
        self.name = name
        self.children = []

    def Add(self, comp):
        self.children.append(comp)

    def Remove(self,comp):
        pass
        self.children.remove(comp)

    def Display(self, deph):
        strTemp = ""
        for i in range(deph):
            strTemp += strTemp + "-"
        print deph, self.name

if __name__ == '__main__':
    pass
    #生成树根
    root = Composite("这里是树根")
    root.Add("叶子1")
    root.Add("叶子2")
    root.Display(5)
    comp = Composite("Composite X")
    comp = ""