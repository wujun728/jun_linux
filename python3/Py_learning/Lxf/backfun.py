#!/usr/bin/python3
def count():
	def f(j):
		def g():
			print('在g()内部，--调用的时候才走到g内部')
			return j*j
		print('f()中，--执行了f了')
		return g
	fs=[]
	for i in range(1,4):
		fs.append(f(i))
	print('count()中--执行count了')
	print('-----------看一下fs是什么------------')
	print(fs)
	return fs

print('===================================看一下f1, f2, f3 = count()这句话的执行============================================')
f1,f2,f3=count()
print('=======================================下面执行f1、f2、f3的调用========================================================')
print('f1()=',f1())
print('f2()=',f2())
print('f3()=',f3())