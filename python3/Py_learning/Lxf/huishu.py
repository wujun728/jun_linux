#!/usr/bin/python3
def is_palindrome(n):
	if n>10:
		str_n=str(n) #将数字转换为字符串
		'''
		tem=''
				for c in str_n:
			tem=c+tem #逐个读取字符吕，并将顺序反置赋给tem
		'''
		return str_n[:]==str_n[::-1] #str_n[::-1]将str_n列表反置

#if __name__=='__main__':
output=filter(is_palindrome,range(1,1000))
print(list(output))
print(__name__)