import matplotlib
matplotlib.use('GTKAgg')
from matplotlib.backends.backend_gtk import DialogLineprops

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

def f(t):
    s1 = np.cos(2*np.pi*t)
    e1 = np.exp(-t)
    return np.multiply(s1, e1)

def drew(xdata,ydata):
    t1 = np.array(xdata)
    t1_1 = np.array(ydata)
    t2 = np.array(xdata)
    t2_2 = np.array(ydata)

    fig, ax = plt.subplots()
    l1, = ax.plot(t1, t1_1, 'bo', label='line 1')
    l2, = ax.plot(t2, t2_2, 'k--', label='line 2')

    dlg = DialogLineprops([l1,l2])
    dlg.show()
    plt.show()

if __name__ == "__main__":
    if sys.argv[4] == "\\t":
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),"\t")
    else:
        xdata,ydata = dataset(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
    drew(xdata,ydata)
