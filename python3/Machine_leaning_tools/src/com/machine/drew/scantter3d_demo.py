import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys

def dataset(filename,x,y,z,splittype):
    fr = open(filename)
    xdata = []
    ydata = []
    zdata = []
    for line in fr.readlines():
        data = line.strip().split(splittype)
        if x > 0:
            xdata.append(float(data[x-1]))
        if y > 0:
            ydata.append(float(data[y-1]))
        zdata.append(float(data[z-1]))
    if x == 0:
        xdata = range(len(zdata))
    if y == 0:
        ydata = range(len(zdata))       
    return xdata,ydata,zdata

def drew(xdata,ydata,zdata):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = np.array(xdata)
    ys = np.array(ydata)
    zs = np.array(zdata)
    ax.scatter(xs, ys, zs, c='r', marker=(5,1))

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()

if __name__ == "__main__":
    if sys.argv[5] == "\\t":
        xdata,ydata,zdata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),"\t")
    else:
        xdata,ydata,zdata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5])
    drew(xdata,ydata,zdata)
