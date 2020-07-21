#!/usr/bin/python3
def _odd_iter():
	'''构造一个从3开始的奇数列

	这是一个生成器，并且是一个无限的序列'''
	n=1
	while  True:
		n=n+2
		yield n

def _not_divisible(n):
	'''定义一个筛选函数，该函数确定一个数字无法被某个数整除'''
	return lambda x:x%n>0

def primes():
	'''定义一个生成器，不断返回下一个素数'''
	yield 2
	it=_odd_iter() #初始化序列
	while True:
		n=next(it) #返回序列的第一个数
		yield n
		it=filter(_not_divisible(n),it) #构造新序列

for n in primes():
	'''打印1000以内的素数'''
	if n<1000:
		print(n)
	else:
		break