#!/usr/bin/python3
def triangles():
	'''输出杨辉三角。

	把每一行看做一个list，通过generator不断输出下一行list.
	最开始是  N【1】
	然后 N.append(0)  就变成了 【1，0】
	那个循环长度为2
	那么第一次 新N【0】=N【-1】+N【0】=1（N【-1】就是倒数最后一个元素）
    	 第二次 新N【1】=N【0】+ N【1】=1
 	所以此时的N 就是 【1，1】

	以此类推 第二排  N=【1，1，0】（循环次数等于长度）

	第一次循环 新N【0】=N【-1】+N【0】=1
           新N【1】=N【0】+N【1】=2
           新 N【2】=N【1】+N【2】=1'''
	N=[1]
	while True:
		yield N
		N.append(0)
		N=[N[i-1]+N[i] for i in range(len(N))]


#以下测试程序
n=0
for t in triangles():
	print(t)
	n=n+1
	if n==10:
		break