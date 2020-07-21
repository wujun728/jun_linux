#!/usr/bin/python
# -*- coding:UTF-8 -*-

from abc import ABCMeta, abstractmethod

__author__ = "王志鹏"

# 追求者
class Pursuit:
    def __init__(self, name):
        self.name = name

    def giveFlowers(self):
        print self.name + "送你鲜花"
        return self.name + "送你鲜花"

    def giveChocolate(self):
        print self.name + "送你巧克力"
        return self.name + "送你巧克力"

    def giveDolls(self):
        print self.name + "送你洋娃娃"
        return self.name + "送你洋娃娃"


# 代理者
class Proxy(Pursuit):
    def __init__(self, name):
        self.name = name
        self.pursuit = Pursuit(name)

    def sgiveFlowers(self):
        print self.name + "代理送你鲜花"
        return self.pursuit.giveFlowers()

    def sgiveChocolate(self):
        print self.name + "代理送你巧克力"
        return self.pursuit.giveChocolate()

    def sgiveDolls(self):
        print self.name + "代理送你洋娃娃"
        return self.pursuit.giveDolls()


class Girl:
    def __init__(self, name, gift):
        self.name = name
        self.gift = gift


if __name__ == '__main__':
    # pursuit = Pursuit("小王")
    # pursuit.giveFlowers()

    Proxy = Proxy("小王")
    Proxy.sgiveFlowers()
