#!/usr/bin/python3
class Fib(object):
	"""docstring for Fib"""
	def  __getitem__(self,n):
		if isinstance(n,int):#n是索引
			a,b=1,1
			for x in range(n):
				a,b=b,a+b
			return a
		if isinstance(n,slice):#n是切片
			start=n.start
			stop=n.stop
			if start is None:
				start=0
			a,b=1,1
			L=[]
			for x in range(stop):
				if x>=start:
					L.append(a)
				a,b=b,a+b
			return L

f=Fib()
f[0]
print(f[0:5])