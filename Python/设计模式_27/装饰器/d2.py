#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/19 14:09
# @Author  : Aries
# @Site    : 
# @File    : d2.py
# @Software: PyCharm

class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.__score = score
    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score

s = Student('Bob', 59)
s.score=10
print s.name
print s.score