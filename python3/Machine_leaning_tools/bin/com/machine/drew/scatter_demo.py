"""
Simple demo of a scatter plot.
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
    x = np.array(xdata)
    y = np.array(ydata)
    colors = np.random.rand(len(ydata))
    area = np.pi * (20 * np.random.rand(len(ydata)))**1

    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.show()

if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),"\t")
    else:
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
    drew(xdata,ydata)
