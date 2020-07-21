import matplotlib.pyplot as plt
import  numpy as np

x = np.linspace(-5, 5, 30)

y1 = 2*x + 1
y2 = x**2

plt.figure()
plt.plot(x, y1)
plt.plot(x, y2, color="red", linestyle="--", linewidth=1.0)

# 定义x轴取值范围
plt.xlim((-1, 2))
# 定义y轴的取值范围
plt.ylim((-2, 3))

plt.xlabel("I am x label")
plt.ylabel("I am y label")

# 用于替换单位的小标
new_ticks = np.linspace(-1, 2, 5)
plt.xticks(new_ticks)

# 替换成文字
plt.yticks([-2, -1.8, -1, 1.22, 3 ], ['really bad', 'bad', 'normal', 'good', 'really good'])

# gca = 'get current axis'   获取当前的坐标轴
axis = plt.gca()

# 轴的脊梁  下面是把右边和上面颜色取消
axis.spines['right'].set_color('none')
axis.spines['top'].set_color('none')

axis.xaxis.set_ticks_position('bottom')
axis.yaxis.set_ticks_position('left')

# 坐标轴改变位置的方式
axis.spines['bottom'].set_position(('data', 0)) # outward, axes: 要定位到百分多少
axis.spines['left'].set_position(('data',0))


plt.show();