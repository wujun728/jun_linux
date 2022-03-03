#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2018/11/20 15:22
# @Author  : Aries
# @Site    : 
# @File    : d3.py
# @Software: PyCharm

def catch_exception(origin_func,ss):
    def wrapper(self,a,b,c):
        try:
            u = origin_func(self,a,b,c,ss)
            return u
        except Exception:
            print a,b,c,"EX",ss
    return wrapper


class Test(object):
    def __init__(self):
        pass

    def revive(self):
        print('revive from exception.')
        # do something to restore
    #wait=wait_fixed(5)
    @catch_exception(ss="teststr")
    def read_value(self ,a,b,c):
        print('here I will do something.')
        # print  1/0
        # do something.

    def main(self):
        self.read_value("aa","bb","cc")
if __name__ == '__main__':
    aa = Test()
    aa.main()
    pass
