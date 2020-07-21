import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
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
# the random data
    x = np.array(xdata)
    y = np.array(ydata)

    nullfmt = NullFormatter()         # no labels

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(1, figsize=(8, 8))

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)

    # the scatter plot:
    axScatter.scatter(x, y)
    
    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])
    lim = (int(xymax/binwidth) + 1) * binwidth

    axScatter.set_xlim((-lim, lim))
    axScatter.set_ylim((-lim, lim))

    bins = np.arange(-lim, lim + binwidth, binwidth)
    axHistx.hist(x, bins=bins)
    axHisty.hist(y, bins=bins, orientation='horizontal')

    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())

    plt.show()

if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),"\t")
    else:
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
    drew(xdata,ydata)
