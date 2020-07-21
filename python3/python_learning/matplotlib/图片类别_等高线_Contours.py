import matplotlib.pyplot as plt
import numpy as np

# 等高线，高度计算公式
def f(x,y):
    return (1 - x / 2 + x**5 + y**3) * np.exp(-x**2 -y**2)

n = 256
x = np.linspace(-3, 3, n)
y = np.linspace(-3, 3, n)

# 生成网格图
X,Y = np.meshgrid(x, y)

# cmap 表示颜色的映射map， map成 cool的颜色库
plt.contourf(X, Y, f(X, Y), 8, alpha=0.75, cmap=plt.cm.cool)

# 绘制等高线的线   8: 表示分多少部分
C = plt.contour(X, Y, f(X, Y), 8, colors='black', linewidth=.5)
# 增加标签
plt.clabel(C, inline=True, fontsize=10)

plt.xticks(())
plt.yticks(())

plt.show()