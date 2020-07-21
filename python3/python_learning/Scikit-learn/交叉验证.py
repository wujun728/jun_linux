from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
x = iris.data
y = iris.target

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=4)

# n_neighbors=5  考虑数据点附近的5个点
knn = KNeighborsClassifier(n_neighbors=5)

# 训练模型
knn.fit(x_train, y_train)

# 计算得分
print(knn.score(x_test, y_test))

# 这里是使用交叉验证的方法，  cv  表示分成五组
scores = cross_val_score(knn, x, y, cv=5, scoring='accuracy')
# 综合了5个，进行平均取值
print(scores.mean())