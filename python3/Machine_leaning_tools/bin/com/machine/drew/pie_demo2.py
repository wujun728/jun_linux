"""
Make a pie charts of varying size - see
http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pie for the docstring.

This example shows a basic pie charts with labels optional features,
like autolabeling the percentage, offsetting a slice with "explode"
and adding a shadow, in different sizes.

"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import sys

# Some data
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
    labels = xdata
    fracs = ydata
    patches, texts, autotexts = plt.pie(fracs, labels=labels,autopct='%1.1f%%',shadow=True)

    for t in texts:
        t.set_size('smaller')
    for t in autotexts:
        t.set_size('x-small')
    autotexts[0].set_color('y')

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
