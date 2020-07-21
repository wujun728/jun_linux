import numpy as np
import pyspark

arr0 = np.array(range(10))
print(arr0);

# 创建一个二维数组
arr = np.array([[1,2,3] ,[1,2,3] ,[1,2,3] ] );
print(arr);
# 秩的个数
print(arr.ndim);
# 类型
print(arr.dtype)
# 维度
print(arr.shape);
# 元素个数
print(arr.size)

# 初始化一个数组
arr2 = np.arange(100).reshape(20, 5);

print(arr2);

#  取第一列
print(arr2[:,0])
print("------------")

# 取第一行 和 第四行    第三个参数是步数
print(arr2[0:10:3]);

#  取第一行和第四行
# print(arr2[[0,3]])

# 取 0 到4 列
# print(arr2[0:, [0,4]])

#  取 2,3 行， 2,3 列
print(arr2[[2,3], 1:3])

# 生成10个正态分布随机数
list = np.random.randn(10)
print(list);

reshape_List = list.reshape(5,2)
print(reshape_List);


arr = np.array(range(9)).reshape(3,3);
print(arr);
arr[:,1] = arr[:,1] + 1;
print(arr);