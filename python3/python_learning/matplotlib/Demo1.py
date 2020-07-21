import numpy as np
import matplotlib.pyplot as plt

# 制作一点数据，从-1 到 1 的50个点
x = np.linspace(-1, 1, 50)
# 定义方程
y = 2*x + 1
# 参数是 横坐标的值和纵坐标的值
plt.plot(x, y)
# 显示图像
plt.show()

