"""
Demo of scatter plot on a polar axis.

Size increases radially in this example and color increases with angle (just to
verify the symbols are being scattered correctly).
"""
import numpy as np
import matplotlib.pyplot as plt
import sys

def dataset(filename,x,y,splittype):
    fr = open(filename)
    xdata = []
    ydata = []
    for line in fr.readlines():
        data = line.strip().split(splittype)
        if x > 0:
            xdata.append(float(data[x-1]))
        ydata.append(float(data[y-1]))
    if x == 0:
        xdata = range(len(ydata))
    return xdata,ydata

def drew(xdata,ydata):
    r = np.array(ydata)
    theta = np.array(xdata)
    area = 20 * r**1 * np.random.rand(len(xdata))
    colors = theta

    ax = plt.subplot(111, projection='polar')
    c = plt.scatter(theta, r, c=colors, s=area, cmap=plt.cm.hsv)
    c.set_alpha(0.75)

    plt.show()


if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),"\t")
    else:
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
    drew(xdata,ydata)
