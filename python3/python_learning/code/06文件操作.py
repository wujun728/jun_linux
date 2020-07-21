'''
Created on 2018年10月9日

@author: Administrator
'''
f=open("e:\wc.txt", "rb")
a=f.readline()
print(a)
# position=f.tell()
# print(position)
a=f.readline()
print(a)
a=f.readline()
print(a)
a=f.readline()
print(a)
a=f.readline()
print(a)
a=f.readline()
print(a)
f.seek(-3,2)
print("*"*50)
a=f.readline()
print(a)
f.close()
# 
# # f=open(r"e:\test.txt",'w')
# # f.write("python is simple")
# # f.close()

import os
print(os.name)
print(os.getcwd())
print(os.listdir("d:"))
# os.remove("e:\\test.txt")
