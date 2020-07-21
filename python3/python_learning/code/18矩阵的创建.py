'''
Created on 2018年10月10日

@author: Administrator
'''
import numpy as np
# arr=np.array([[1,2,3],[4,5,6]])
# print(arr)
# print(arr.ndim)
# print(arr.dtype)
# print(arr.shape)
# print(arr.size)
# arr=np.array([[[1,2],[3,4],[5,6]],[[7,8],[9,10],[10,11]]])
# print(arr)
# print(arr.ndim)
# print(arr.dtype)
# print(arr.shape)
# print(arr.size)
# arr=np.arange(10).reshape(2,5)
# arr=np.arange(27).reshape(3,3,3)
# arr=np.random.randn(2,3)
# arr=np.zeros((2,3))
# arr=np.ones((2,3))
# arr=np.empty((2,3))
# print(arr)
# arr=np.arange(10).reshape(2,5)
# print(arr)
# print(np.where(arr>5,arr,0))
# arr=np.random.randint(1,10,20).reshape(4,5)
# brr=np.random.randint(1,10,20).reshape(5,4)
# print(arr)
# print(brr)
# print(arr[0,0])
# print(arr[:,0])
#第一行和第四行
# print(arr[0:4:3])
# print(arr[[0,3]])
# #第一列和第四列
# print(arr[0:,0:5:4])
# print(arr[0:,[0,4]])
#第二三行，第二三列
# print(arr[[1,2]])
# print(arr[[1,2],1:3])
# print(arr[0][0])
# print(arr.shape[0])
# for i in range(0,arr.shape[0]):
#     for j in range(arr.shape[1]):
#         print(arr[i][j],end=" ")
# print(arr.sum())
# print((arr>5).sum())
# print(arr.sum(0))
# print(arr.sum(1))
# print(arr+brr)
# print(np.dot(arr,brr))
# print(arr.T)
# a = np.arange(10).reshape(2,5)
# print(a)
# a.resize(5,2)
# print(a)
b = np.arange(6).reshape(2,3)
c = np.ones((2,3))
# d = np.hstack((b,c))   
# print(d)           # hstack：horizontal stack 左右合并
# e = np.vstack((b,c)) 
# print(e)             # vstack: vertical stack 上下合并          
# f = np.column_stack((b,c))
# print(f)
# g = np.row_stack((b,c))
# print(g)
# h = np.stack((b, c), axis=1)      # 按行合并
# print(h)
i = np.stack((b,c), axis=0)       # 按列合并
print(i)
# j = np.concatenate ((b, c, c, b), axis=0)   #多个合并
# print(j)
# 
# #分割
k = np.hsplit(i, 2)
print(k)
l = np.vsplit(i, 2)
print(l)
# m = np.split(i, 2, axis=0)
# n = np.split(i, 2,axis=1)
# 
# o = np.array_split(np.arange(10),3)   #不等量分割

