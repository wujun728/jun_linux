#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2019/1/6 10:10
# @Author  : 王志鹏
# @Site    :
# @File    : d2.py
# @Software: PyCharm

from abc import ABCMeta, abstractmethod


# 紧耦合的程序演化
# 1.如果现在有一个N品牌的手机,它有一个小游戏,我要玩游戏
# 2.增加M品牌的手机,也玩游戏
# 3.增加通讯录功能
# 试想如果再增加品牌,功能呢:
"""
对象的继承关系是在编译时就订好了,所以在无法在运行时改变从父类继承的实现.
子类的实现与它的父类有非常紧密的依赖关系,以至于父类实现中的任何变化必然会导致子类发生变化.当你需要复用子类时,如果继承下来的实现不适合解决新的
问题,则父类必须重写或被其他更适合的类替换.这种依赖关系限制了灵活性并最限制了复用性;

合成/聚合复用原则: 尽量使用合成/聚合,尽量不要使用继承
聚合表示一种 弱 的'拥有'关系,体现的是A对象可以包含B对象,但B对象不是A对象的一部分;
合成则是一种 强 的'拥有'关系,体现了严格的部分和整体关系,部分和整体的生命周期一样

合成/聚合复用原则使用的好处是: 优先使用对象的合成/聚合将有帮助你保持每个类被封装,并集中在单个任务上.这样的类和类继承层次会保持较小规模
并不太可能增长为不可控制的庞然大物
"""
class phoneBrand(object):
    def run(self): pass

# class Game(object):
#     __metaclass__ = ABCMeta
#
#     @abstractmethod
#     def playGame(selfe): pass


class Nphone(phoneBrand):
    pass

class Mphone(phoneBrand):
    pass

class NGame(Nphone):
    def run(self):
        print "运行N牌手机游戏"


class MGame(Mphone):
    def run(self):
        print "运行M牌手机游戏"


class NaddressList(Nphone):
    def run(self):
        print "运行N牌手机通讯录"


class MaddressList(Mphone):
    def run(self):
        print "运行M牌手机通讯录"


if __name__ == '__main__':
    ab = phoneBrand()

    ab = NGame()
    ab.run()

    ab = NaddressList()
    ab.run()

    ab = MGame()
    ab.run()

    ab = MaddressList()
    ab.run()