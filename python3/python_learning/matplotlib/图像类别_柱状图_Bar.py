import matplotlib.pyplot as plt
import numpy as np

n = 12
X = np.arange(n)
# uniform： 会产生一个0.5-1.0 的随机变量
Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)

# 画一个向上和向下的曲线  用facecolor设置主体颜色，edgecolor设置边框颜色为白色
plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

# zip：是把X,Y1的值，分别传入到 x,y中
for x, y in zip(X, Y1):
    #偏上一点，增加文字   ha: horizontal alignment(对齐方式)
    plt.text(x+0.04, y+0.05, '%.2f'%y, ha='center', va='bottom')

for x, y in zip(X, Y2):
    # 偏上一点，增加文字   ha: horizontal alignment(对齐方式)
    plt.text(x - 0.04, -y - 0.05, '-0154%.2f' % y, ha='center', va='top')


plt.xlim(-.5, n)
plt.xticks(())
plt.ylim(-1.25, 1.25)
plt.yticks(())

plt.show()