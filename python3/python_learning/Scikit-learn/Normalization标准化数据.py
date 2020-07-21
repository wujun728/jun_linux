from sklearn import preprocessing
import numpy as np
# 将数据集分成 训练集 和测试集的模块
from sklearn.cross_validation import train_test_split
# 生成一些数据
from sklearn.datasets.samples_generator import make_classification
# SVC模型
from sklearn.svm import SVC
import matplotlib.pyplot as plt

a = np.array([[10, 2.7, 3.6],
              [-100, 5, -2],
              [120, 20, 40]])
print(a)
# 相当于做了归一化
print(preprocessing.scale(a))

# 生成一些数据    n_features： 表示两个属性   n_informative: 两个比较相关的属性   random_state：随机产生的data
x, y  = make_classification(n_samples=300, n_features=2, n_redundant=0, n_informative=2, random_state=22,
                            n_clusters_per_class=1, scale=100)
# plt.scatter(x[:, 0], x[:,1], c=y)
# plt.show()

# 进行归一化处理, 压缩到-1 到 1之间
x = preprocessing.minmax_scale(x, feature_range=(-1, 1))

# 将数据分成 train 和test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

clf = SVC()

clf.fit(x_train, y_train)

print(clf.score(x_test, y_test))