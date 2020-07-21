#！/usr/bin/python3
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_name(t):
	return t[0].lower()   #key函数作用于L中的元素，也就是说t代表的是三个（），所以t[0]代表的才是（）中的第一个元素名字
l2=sorted(L,key=by_name)
print('按姓名排序：',l2)

def by_scort(t):
	return t[1]
l3=sorted(L,key=by_scort,reverse=True) #reverse=True表示倒序排序
print('按成绩排序：',l3)

