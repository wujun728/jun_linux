#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/9/16 14:53
# @Author  : 王志鹏
# @Site    : 
# @File    : d1.py
# @Software: PyCharm

# 第一版双向耦合代码

# 秘书类
class Secretary():
    def __init__(self):
        self.people = []
        self.action = ""

    def addPeople(self, people):
        self.people.append(people)

    # 通知
    def Notify(self):
        for i, v in enumerate(self.people):
            v.Updata()

    # 前台状态
    def SecretaryAction(self, actiom):
        self.action = actiom


# 看股票观看者
class StockObserver():
    def __init__(self, name, sub):
        self.name = name
        self.sub = sub

    def Updata(self):
        print "%s,%s,关闭股票行情,继续工作" % (self.sub.action, self.name)


# 解耦实践一



if __name__ == '__main__':
    # 前台
    secretary = Secretary()
    # 看股票的同事
    stockobserver1 = StockObserver("小王", secretary)
    stockobserver2 = StockObserver("小李", secretary)

    secretary.addPeople(stockobserver1)
    secretary.addPeople(stockobserver2)
    # 发现老板回来改变状态
    secretary.SecretaryAction("老板回来了!")
    # 通知人员
    secretary.Notify()
