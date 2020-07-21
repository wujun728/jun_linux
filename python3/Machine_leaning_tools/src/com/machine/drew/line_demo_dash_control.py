"""
Demo of a simple plot with a custom dashed line.

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
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
    #x = np.linspace(0, 10)
    line, = plt.plot(xdata, ydata, '-', linewidth=1)

    plt.show()

if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),"\t")
    else:
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
    drew(xdata,ydata)
