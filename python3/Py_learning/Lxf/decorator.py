#!/usr/bin/python3
import functools
import time
def log(textOrFunc):
	'''在函数调用前后打印一行日志'''
	text=textOrFunc if isinstance(textOrFunc,str) else 'call' # 对text进行赋值，如果textOrFunc不是客串，就将text赋值call
	
	def decorator(func):
		print('程序开始：')
		@functools.wraps(func)		
		def wrapper(*args,**kw):
			print('%s %s():'%(text,func.__name__))
			r=func(*args,**kw)
			print('程序结束！')
			return r			
		return wrapper
	return decorator if isinstance(textOrFunc,str) else decorator(textOrFunc)
'''=======================================================
  下面是测试
  ======================================================='''
print('测试一：')
@log
def now():
	print(time.strftime('%Y-%m-%d'))
now()

print('测试二：')
@log('开始函数')
def tim():
	print(time.strftime('%H:%M:%S'))
tim()
