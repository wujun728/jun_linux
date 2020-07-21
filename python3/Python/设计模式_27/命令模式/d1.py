#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2019/1/6 13:41
# @Author  : 王志鹏
# @Site    : 
# @File    : d1.py
# @Software: PyCharm

"""
命令模式 Command: 将一个请求封装为一个对象,从而使你可用不得请求对客户进行参数化;
对请求排队或记录请求日志,以及支持可撤销的操作.
命令模式作用:
1.他能较容易地设计一个命令队列
2.在需要的情况下可以较容易的将命令计入日志
3.允许接受请求的一方就决定是否要否决请求
4.可以容易地实现对请求的撤销和重做
5.由于加进新的具体命令类不影响其他的类,因此增加新的具体命令类很容易
6** 命令模式把请求一个操作的对象与知道怎么执行一个操作对象分割开!!!

敏捷开发原则告诉我们:不要为代码添加基于猜测的,实际不需要的功能.如果不清楚一个系统是否需要命令模式,一般不要着急实现它,
事实上在需要的时候通过重构实现这个模式并不困难,只有在真正需要如撤销/恢复操作功能时,把原来的代码重构为命令模式才有意义.
"""
# 抽象命令
from abc import *


class Command(object):
    __metaclass__ = ABCMeta

    def __init__(self, barbecuer):
        self.barbecuer = barbecuer

    @abstractmethod
    def excuteCommand(self): pass


# 具体命令类
class BakeMuttonCommand(Command):
    def excuteCommand(self):
        print "通知烤肉工>>烤肉串"
        self.barbecuer.excute()


# 烤鸡翅命令类
class BakeChickenWingCommand(Command):
    def excuteCommand(self):
        print "通知烤肉工>>烤鸡翅"
        self.barbecuer.excute()


# 烤肉串者
class Barbecuer(object):
    def excute(self):
        print "开始烤串"


# 服务员
class Waiter(object):
    def __init__(self):
        self.command = None

    def setOrder(self, command):
        self.command = command

    def Notify(self):
        self.command.excuteCommand()


if __name__ == '__main__':
    barbecuer = Barbecuer()  # 烤串者
    command1 = BakeMuttonCommand(barbecuer) #烤肉串
    command2 = BakeChickenWingCommand(barbecuer) #烤肉串
    waiter = Waiter()#服务员

    waiter.setOrder(command1)
    waiter.Notify()

    waiter.setOrder(command2)
    waiter.Notify()
