import matplotlib.pyplot as plt

plt.figure()

# 将图片变成 2行2列   第三个参数，表示在第几个
plt.subplot(2, 2, 1)
plt.plot([0,1], [0,1])

# 第二行图
plt.subplot(2, 2, 2)
plt.plot([0,1], [0,2])

# 第三张
plt.subplot(2, 2, 3)
plt.plot([0,1], [0,2])

# 第四张
plt.subplot(2, 2, 4)
plt.plot([0,1], [0,2])


plt.figure()
# 将图片变成 2行1列   第三个参数，表示在第几个
plt.subplot(2, 1, 1)
plt.plot([0,1], [0,1])

# 第二行图
plt.subplot(2, 3, 4)
plt.plot([0,1], [0,2])

# 第三张
plt.subplot(2, 3, 5)
plt.plot([0,1], [0,2])

# 第四张
plt.subplot(2, 3, 6)
plt.plot([0,1], [0,2])

plt.show()