#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/16 16:19
# @Author  : DanBrown
# @Site    : https://www.cnblogs.com/cicaday/p/python-decorator.html
# @File    : d1.py
# @Software: PyCharm
class Student(object):

    def get_score(self):
        return self._score

    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
if __name__ == '__main__':

    s = Student()
    s.set_score(22)
    print s.get_score()