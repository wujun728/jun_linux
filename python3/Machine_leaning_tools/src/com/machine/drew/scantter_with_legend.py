import matplotlib.pyplot as plt
from numpy.random import rand
import numpy as np
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
    x, y = np.array(xdata),np.array(ydata)
    scale = 100.0 * rand(len(ydata))
    plt.scatter(x, y, c='blue', s=scale, label='blue',alpha=0.5, edgecolors='none')

    plt.legend()
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),"\t")
    else:
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
    drew(xdata,ydata)
