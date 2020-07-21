
from numpy import *

import sys

def loadset(filename,n,splittype):
    fr = open(filename)
    datamat = []
    i = int(n)
    for line in fr.readlines():
        lines = line.strip().split(splittype)
        datamat.append(float(lines[i-1]))
    return datamat

def test(filename,n,splittype):
    datamet = loadset(filename,n,splittype)
    average = var(mat(datamet))
    print 'average is : ' + str(average)

if __name__ == "__main__":
	if sys.argv[3] == "\\t":
		test(sys.argv[1],int(sys.argv[2]),"\t")	
	else:	
		test(sys.argv[1],int(sys.argv[2]),sys.argv[3])
