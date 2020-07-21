import matplotlib.pyplot as plt
import numpy as np

# 用这样 3x3 的 2D-array 来表示点的颜色，每一个点就是一个pixel（像素）
a = np.array([0.313660827978, 0.365348418405, 0.423733120134,
              0.365348418405, 0.439599930621, 0.525083754405,
              0.423733120134, 0.525083754405, 0.651536351379]).reshape(3,3)
#  关于interpolation的值  https://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html
# 图片显示
plt.imshow(a, interpolation='nearest', cmap=plt.cm.bone, origin='lower')
# 显示每个点的颜色值   shrink：表示压缩成百分90
plt.colorbar(shrink=0.9)

plt.xticks(())
plt.yticks(())
plt.show()