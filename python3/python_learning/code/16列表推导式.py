'''
Created on 2018年10月10日

@author: Administrator
'''
for i in range(1,10):
    print(i)
a=[i for i in range(1,10)]
a=[i for i in range(1,10) if i%2==0]
print(a)
b=[(i,j,k) for i in range(1,10) for j in range(1,10) for k in range(1,10)]
print(b)
# c=(i for i in range(1,10))
# print(c[1])
d=(1,2,3)
print(d[1])