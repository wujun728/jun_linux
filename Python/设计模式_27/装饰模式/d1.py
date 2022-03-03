#!/usr/bin/python
# -*- coding:UTF-8 -*-

from abc import ABCMeta, abstractmethod

__author__ = "王志鹏"

class Person():
    def __init__(self, name):
        print '%s开始穿衣' % name


class Finery():
    __metaclass__ = ABCMeta

    @abstractmethod
    def show(self):
        pass


class TShirt(Finery):
    def show(self):
        print '穿TShirst'


class Trouser(Finery):
    def show(self):
        print '穿裤子'


class Shoe(Finery):
    def show(self):
        print '穿鞋子'


class Tie(Finery):
    def show(self):
        print '穿领带'


if __name__ == '__main__':
    person = Person('kevin')
    finerys = []
    finerys.append(TShirt())
    finerys.append(Trouser())
    finerys.append(Shoe())
    finerys.append(Tie())
    # for i, v in enumerate(finerys):
    #     print v.show()
    # print "===="
    map(lambda x: x.show(), finerys)
