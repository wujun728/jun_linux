from sklearn import datasets
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
# 加载房价数据
loaded_data = datasets.load_boston()
data_x = loaded_data.data
data_y = loaded_data.target

# 定义模型
model = LinearRegression()

# 让模型进行学习
model.fit(data_x, data_y)

# 预测值
print(model.predict(data_x[:4, :]))
# 真实值
print(data_y[:4])

# 我们也可以创造一些数据
x, y = datasets.make_regression(n_samples=100, n_features=1, n_targets=1, noise=1)
plt.scatter(x, y)
plt.show()