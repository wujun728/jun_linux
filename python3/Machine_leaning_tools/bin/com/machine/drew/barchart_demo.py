
#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt
import sys

def dataset(filename,x,y,splittype):
    fr = open(filename)
    xdata = []
    ydata = {}
    if y != 'NONE':
        label = y.strip().split(',')
        for i in range(len(label)):
            if label[i].strip() is not None:
                ydata[float(label[i].strip())] = 0
        ydata[float("inf")] = 0
    for line in fr.readlines():
        data = line.strip().split(splittype)
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
    return ydata

def drew(xdata,ydata):
    N = 5
    menMeans = ydata
    menStd = [3]*len(ydata)

    ind = np.arange(len(ydata))  
    width = 0.35      

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

    ax.set_ylabel('Number')
    ax.set_xlabel('range')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(xdata)

    for rect in rects1:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')
    plt.show()

if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        ydata = dataset(sys.argv[1],int(sys.argv[2]),sys.argv[3],"\t")
    else:
        ydata = dataset(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4])
    ylabel = []
    xlabel = ydata.keys()
    xlabel.sort()
    for i in range(len(xlabel)):
        ylabel.append(ydata[xlabel[i]])
    drew(xlabel,ylabel)
