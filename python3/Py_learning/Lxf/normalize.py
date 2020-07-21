#!/usr/bin/python3 
def normalize(name):
	'''将输入不不规范英文信息转换为规范的首字母大写，其他小写的格式'''
	return name[:1].upper()+name[1:].lower()


#下面是测试
l1=['adam','LISA','barT']
l2=list(map(normalize,l1))
print (l2)