#!/usr/bin/python3
from functools import reduce
def prod(L):
	'''利用reduce函数实现对一个list求积'''
	return reduce(lambda  x,y:x*y,L)  #利用lambda返回一个计算积的函数

#下面是测试
print('3*5*7*9=',prod([3,5,7,9]))