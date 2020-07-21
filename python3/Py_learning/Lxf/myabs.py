#!/usr/bin/python3
'''求绝对值函数'''
def my_abs(x):
	'''示绝对值函数
	接受一个整数或浮点数
	返回整数或浮点数的绝对值'''
	if not isinstance(x,(int,float)):
		raise TypeError('bad operand type')
	if x>=0:
		return x
	else:
		return -x
