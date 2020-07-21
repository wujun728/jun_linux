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

# y = 0.1x + 0.3
print(model.coef_)  # model.coef 输出 0.1 ，  也就是系数

# 输出 0.3  也就是常数.  和y轴的交点
print(model.intercept_)

# model中学习到的东西，我们进行打分
# data_x预测， data_y对比
# 这里使用 R^2的方式进行打分
print(model.score(data_x, data_y))

# 拿出原来model中定义的参数
print(model.get_params())

# 预测值
# print(model.predict(data_x[:4, :]))
