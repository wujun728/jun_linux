import matplotlib.pyplot as plt
import numpy as np

# 给图增加描述框

# 制作一点数据，从-1 到 1 的50个点
x = np.linspace(-3, 3, 50)
# 定义方程
y1 = 2*x + 1
y2 = x**2

plt.figure(num=1, figsize=(8, 5))
# linestyle：表示风格
l1, = plt.plot(x, y1, color='red', linewidth=1.0, linestyle="--", label="up")
l2, = plt.plot(x,y2, label="down")

# 首先需要配置label， 然后在使用legend方法
# handles
# parm1： loc:位置  默认best，寻找出最好的位置
# 使用handles替换 label
plt.legend(handles=[l1,l2], labels=['aaa', 'bbb'], loc="best")

plt.show()