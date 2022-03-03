#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/21 10:26
# @Author  : 王志鹏
# @Site    : 
# @File    : 委托.py
# @Software: PyCharm

class A:
    def f_one(self, x):
        print"here is f_one"
        print"x=",x
        print"-"*100

    def f_two(self):
        print"here is f_two"
        print"-"*100

class B(A):
    def __init__(self):
        self._a = A()

    def f_three(self):
        pass

    def __getattr__(self, name):#相当于重写了__getattr__,利用__getattr_来实现委托的效果（其实委托就是甩锅的意思啦，B搞不定，甩锅给A）
        # print name,"???"
        return getattr(self._a, name)

if __name__ == '__main__':
    b_test=B()
    x=6
    b_test.f_one(x)
    b_test.f_two()