import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 3D 图
# 首先在进行 3D Plot 时除了导入 matplotlib ，还要额外添加一个模块，即 Axes 3D 3D 坐标轴显示：

# 定义图片的窗口
fig = plt.figure()
ax = Axes3D(fig)

# 定义X和Y的值
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)    # x-y 平面的网格
R = np.sqrt(X ** 2 + Y ** 2)
# 通过X和Y，生成Z的高度图
Z = np.sin(R)

# plot 3D的方式，也就是绘制3D的方法
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.rainbow)

ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap='rainbow')
ax.set_zlim(-2, 2)

plt.show()