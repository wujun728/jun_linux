#!/usr/bin/python3
count=0 #定义一个计数器，用于计算移动的次数
def hanoi(n,a,b,c):
	'''通过递归函数实现汉诺塔的移动过程.

		可以将函数简单的理解为，将a柱上的n个饼通过b柱移动到c柱上去;
		1、第一步将a柱上的n-1个饼通过c柱移动到b柱
		2、第二步将a柱上的最底下一个饼从a柱移动到c柱
		3、第三步将刚移动到b柱上的n-1个饼再通过a柱移动到c柱上去'''
	global count             #将count定义为全局
	if n<1:
		raise('阶数不允许为小于1的数！')
	if n==1:
		print(a,'-->',c) #特殊情况，只有一个饼的时候直接从A柱移动到C柱
		count+=1
	else:
		hanoi(n-1,a,c,b) #相当于将n-1个饼从A柱通过C柱移动到B柱
		print(a,'-->',c) #替换下行的递归调用
		#hanoi(1,a,b,c)   #将A柱最底下的一个饼从A柱移到C柱
		hanoi(n-1,b,a,c) #再将B柱上的n-1个饼通过A柱移动到C柱
	
n=int(input('请输入汉诺塔的层数>>'))
hanoi(n,'A','B','C')
print('移动次数=',count)
