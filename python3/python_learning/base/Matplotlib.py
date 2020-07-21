import matplotlib.pyplot as plt
import numpy as np

data = np.arange(10)

print(data);

plt.plot(data);

# plt.show()

fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)