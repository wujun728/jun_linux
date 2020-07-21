#!/usr/bin/python
# -*- coding:UTF-8 -*-

# @Time    : 2018/9/16 14:08
# @Author  : 王志鹏
# @Site    : 
# @File    : d1.py
# @Software: PyCharm

"""
大话设计模式
设计模式——建造者模式
建造者模式(Builder):将一个复杂对象的构建与它的表示分离,使得同样的构建过程可以创建不同的表示
特性: 指挥者(Director) 指挥 建造者(Builder) 建造 Product
建造者模式是在创建复杂对象的算法应该独立于该对象的组成部分以及他们的装配方式时适用的模式
"""

import abc

#建造者
class Builder(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_header(self):
        pass

    @abc.abstractmethod
    def create_body(self):
        pass

    @abc.abstractmethod
    def create_hand(self):
        pass

    @abc.abstractmethod
    def create_foot(self):
        pass

class Thin(Builder):
    def create_header(self):
        print '瘦子的头'

    def create_body(self):
        print '瘦子的身体'

    def create_hand(self):
        print '瘦子的手'

    def create_foot(self):
        print '瘦子的脚'

class Fat(Builder):
    def create_header(self):
        print '胖子的头'

    def create_body(self):
        print '胖子的身体'

    def create_hand(self):
        print '胖子的手'

    def create_foot(self):
        print '胖子的脚'

#指挥者
class Director(object):
    def __init__(self, person):
        self.person = person

    def create_preson(self):
        self.person.create_header()
        self.person.create_body()
        self.person.create_hand()
        self.person.create_foot()


if __name__ == "__main__":
    thin = Thin()
    fat = Fat()

    director_thin = Director(thin)
    director_fat = Director(fat)

    director_thin.create_preson()
    director_fat.create_preson()
