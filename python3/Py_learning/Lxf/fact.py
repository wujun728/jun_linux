#!/usr/bin/python3
def fact(n):
	'''计算阶乘函数：fact(n)=n!=1X2X3X....X(n-1)Xn=(n-1)!Xnfact(n-1)Xn'''
	return fact_iter(n,1)	

def fact_iter(num,product):
	if num==1:
		return product
	return fact_iter(num-1,num*product)
