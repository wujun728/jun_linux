import matplotlib.pyplot as plt
import numpy as np
# Figure相当于一个大图框

# 制作一点数据，从-1 到 1 的50个点
x = np.linspace(-3, 3, 50)
# 定义方程
y1 = 2*x + 1
y2 = x**2

plt.figure(num=1, figsize=(8, 5))
# linestyle：表示风格
plt.plot(x, y1, color='red', linewidth=1.0, linestyle="--")

plt.figure(num=2, figsize=(8, 5))
plt.plot(x,y2)

plt.show()