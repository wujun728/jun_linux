"""
Demo of bar plot on a polar axis.
"""
import numpy as np
import matplotlib.pyplot as plt
import sys

def dataset(filename,x,y,splittype):
    fr = open(filename)
    xdata = []
    ydata = {}
    maxdata = float('-inf')
    if y != 'NONE':
        label = y.strip().split(',')
        for i in range(len(label)):
            if label[i].strip() is not None:
                ydata[float(label[i].strip())] = 0
        ydata[float("inf")] = 0
    for line in fr.readlines():
        data = line.strip().split(splittype)
        if float(data[x-1]) > maxdata:
            maxdata = float(data[x-1])
        if y == 'NONE':
            if ydata.has_key(float(data[x-1])):
                ydata[float(data[x-1])] = ydata[float(data[x-1])] + 1
            else :
                ydata[float(data[x-1])] = 1
        else:
            i = 0
            label = y.strip().split(',')
            while i < len(label) and float(data[x-1]) > float(label[i].strip()):
                i = i + 1
            if i == len(label):
                ydata[float("inf")] = ydata[float("inf")] + 1
            else:
                ydata[float(label[i].strip())] = ydata[float(label[i].strip())] + 1     
    return ydata,maxdata

def drew(xdata,ydata):
    theta = np.array(xdata)
    radii = np.array(ydata)
    width = np.pi / 8 * np.random.rand(len(ydata))
    colors = np.random.rand(len(ydata))

    ax = plt.subplot(111, projection='polar')
    bars = ax.bar(theta, radii, width=width,color=colors, bottom=0.0)

    for r, bar in zip(radii, bars):
        bar.set_alpha(0.5)

    plt.show()


if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        ydata,maxdata = dataset(sys.argv[1],int(sys.argv[2]),sys.argv[3],"\t")
    else:
        ydata,maxdata = dataset(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4])
    ylabel = []
    xlabel = ydata.keys()
    xlabel.sort()
    for i in range(len(xlabel)):
        ylabel.append(ydata[xlabel[i]])
    xlabel.pop()
    xlabel.append(maxdata)
    print xlabel,ylabel
    drew(xlabel,ylabel)
