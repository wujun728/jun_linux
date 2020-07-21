#!/usr/bin/python3
def power(x,n=2):
	'''求x的n次方函数'''
	s=1
	while n>0:
		n=n-1
		s=s*x
	return s
