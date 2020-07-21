import numpy as np

import random

a = []
for i in range(100):
    a.append(0)

a = np.array(a)

a = a.reshape((10, 10))

for i in range(10):
    if i == 0 :
        continue
    j = random.randint(0, i-1)
    a[i][j] = 1
    a[j][i] = 1
count = 0
while count < 6:

    # 表示随机选中哪一行
    i = random.randint(1, 9)
    isFull = True
    for index in range(i):
        if a[i][index] == 0 :
            isFull = False
            break

    # 表示这一列已经占满了1
    if isFull:
        continue

    while True:
        j = random.randint(0, i - 1)
        if a[i][j] == 0:
            a[i][j] = 1
            a[j][i] = 1
            count = count + 1
            break

print(a)


