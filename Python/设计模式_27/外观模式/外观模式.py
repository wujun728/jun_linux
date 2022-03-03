#!/usr/bin/python
# -*- coding:UTF-8 -*-

"""外观模式(Facade Pattern):为子系统中的一组接口提供一个一致界面,此模式定义一个高层接口,使得子系统更加容易使用"""
__author__ = "王志鹏"

class Stock1:
    def Buy(self):
        print "股票一, 买入"

    def Sell(self):
        print "股票一, 卖出"


class Stock2:
    def Buy(self):
        print "股票二, 买入"

    def Sell(self):
        print "股票二, 卖出"


class Stock3:
    def Buy(self):
        print "股票三, 买入"

    def Sell(self):
        print "股票三, 卖出"


class NationalDebt1():
    def Buy(self):
        print "国债, 买入"

    def Sell(self):
        print "国债, 卖出"


class Realty1:
    def Buy(self):
        print "房地产, 买入"

    def Sell(self):
        print "房地产, 卖出"


# 外观类
class Fund:
    def __init__(self):
        self.Stock1 = Stock1()
        self.Stock1 = Stock2()
        self.Stock1 = Stock3()
        self.NationalDebt1 = NationalDebt1()
        self.Realty1 = Realty1()

    def buy(self):
        self.Stock1.Buy()
        self.Stock2.Buy()
        self.Stock3.Buy()
        self.NationalDebt1.Buy()
        self.Realty1.Buy()

    def sell(self):
        self.Stock1.Sell()
        self.Stock2.Sell()
        self.Stock3.Sell()
        self.NationalDebt1.Sell()
        self.Realty1.Sell()


if __name__ == '__main__':
    pass
