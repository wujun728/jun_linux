import matplotlib.pyplot as plt
import numpy as np

# 为了强调出某个点

x = np.linspace(-3, 3, 50)
y = 2*x + 1

plt.figure()
plt.plot(x, y, label="line")
plt.legend()

# gca = 'get current axis'   获取当前的坐标轴
axis = plt.gca()
# 坐标轴改变位置的方式
axis.spines['bottom'].set_position(('data', 0)) # outward, axes: 要定位到百分多少
axis.spines['left'].set_position(('data',0))

# 添加标注
x0 = 1
y0 = 2*x0 + 1
# 将整个点 plot上去    s: 大小， color：颜色
plt.scatter(x0, y0, s=50, color='red')

# 生成一条线   k--: 表示black，虚线  , lw: 线宽
plt.plot([x0, x0], [y0, 0], 'k--', lw=2.5)

# 方法1
plt.annotate(r'$2x+1=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30),
             textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))

# 方法2
plt.text(-3.7, 3, r'$This\ is\ the\ some\ text.$', fontdict={'size': 16 });

plt.show()