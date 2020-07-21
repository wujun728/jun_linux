#!/usr/bin/python3
def fib(max):
	'''斐波拉契数列（Fibonacci）--除了第一个和最后一个数，任意一个数字都等于前两个数字的和.

	输入一个数值n，将输出n个数'''
	n,a,b=0,0,1
	while n<max:
		print(b)
		a,b=b,a+b
		n+=1
	return 'done'

def fib2(max):
	'''将原有FIB函数转换为一个generator函数'''
	n,a,b=0,0,1
	while n<max:
		yield b
		a,b=b,a+b
		n+=1
	return 'Done!'