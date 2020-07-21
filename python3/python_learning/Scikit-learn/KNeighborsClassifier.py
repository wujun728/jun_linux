import numpy as np
from sklearn import datasets
from sklearn.cross_validation import train_test_split
# 选择邻近的点，模拟出数据的值
from sklearn.neighbors import KNeighborsClassifier

# 加载鸢尾属植物 数据集
iris = datasets.load_iris()
iris_x = iris.data
iris_y = iris.target

print(iris_x[:2, :]);
# 分类，表示有几类
print(iris_y)

# test_size表示测试比例占据整个数据百分多少
x_train, x_test, y_train, y_test = train_test_split(iris_x, iris_y, test_size=0.3)

print(y_train)

# 定义 最近邻分类器 KNeighborsClassifier
knn = KNeighborsClassifier()

# 把数据fit一下，就会自动完成train的步骤了
knn.fit(x_train, y_train)

# 下面的knn，就是已经训练好的knn模型
print(knn.predict(x_test))
# 下面是真实值
print(y_test)