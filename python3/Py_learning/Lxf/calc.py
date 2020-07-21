#!/usr/bin/python3
def calc(*numbers):
	'''计算一组数据的平方和'''
	sum=0
	for n in numbers:
		sum+=n**2
	return sum
