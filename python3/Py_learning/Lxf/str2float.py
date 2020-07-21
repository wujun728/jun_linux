#!/usr/bin/python3
from functools import reduce
def char2num(s):
	'''将字符转换成数字'''
	return{'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]


def str2float(s):
	'''将字符串转换成浮点数'''
	s=list(s)
	if '.' in s:
		dot_len=len(s)-s.index('.')-1   #确定小数点后的长度
		s.remove('.')                                       #将小数点从列表中移除
		return reduce(lambda x,y:x*10+y,map(char2num,s))/(10**dot_len) #将字符串转换成整数后，除以10以点所在位置的次方
	else:
		return reduce(lambda x,y:x*10+y,map(char2num,s))

#下面是结果测试
print('str2float(\'124.456\')=',str2float('124.456'))
