
from numpy import *
import sys

def loadset(filename,n,splittype):
    fr = open(filename)
    datamat = []
    i = int(n)
    mins = float("inf")
    for line in fr.readlines():
        lines = line.strip().split(splittype)
        if mins > float(lines[i-1]):
            mins = float(lines[i-1])
    return mins

def test(filename,n,splittype):
    mins = loadset(filename,n,splittype)
    print 'min is : ' + str(mins)

if __name__ == "__main__":
	if sys.argv[3] == "\\t":
		test(sys.argv[1],int(sys.argv[2]),"\t")
	else:
		test(sys.argv[1],int(sys.argv[2]),sys.argv[3])
