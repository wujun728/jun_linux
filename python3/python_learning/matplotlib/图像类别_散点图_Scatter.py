import matplotlib.pyplot as plt
import numpy as np

N = 1024
X = np.random.normal(0, 1, N)
Y = np.random.normal(0, 1, N)

# 用于颜色生成
T = np.arctan2(Y, X)

# 画散点图
plt.scatter(X, Y, s=75, c=T, alpha=0.5)

# 显示区间
plt.xlim((-1.5, 1.5))
plt.ylim((-1.5, 1.5))

# 隐藏ticks
plt.xticks()
plt.yticks()

plt.show()