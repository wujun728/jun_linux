'''
Created on Jan 8, 2011

@author: Peter
'''
from numpy import *
import sys

def loadDataSet(fileName,splittype):     
    numFeat = len(open(fileName).readline().split(splittype)) - 1 
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split(splittype)
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T*yMat)
    return ws

def pre(trainfile,prefile,outfile,splittype):
    print "running..."
    dataMat,labelMat = loadDataSet(trainfile,splittype)
    ws = standRegres(dataMat,labelMat)
    fw = open(outfile,'a')
    fr = open(prefile)
    for line in fr.readlines():
        data = []
        lines = line.strip().split(splittype)
        for i in range(len(lines)):
            data.append(float(lines[i]))
        dat = mat(data)
        predict = dat*ws
        pre = predict.tolist()
        fw.write(line.strip() + splittype + str(pre[0][0]) + '\n')
    fr.close()
    fw.flush()
    fw.close()
    print "end...."

if __name__ == "__main__":
	if sys.argv[4] == "\\t":
		pre(sys.argv[1],sys.argv[2],sys.argv[3],"\t")
	else:		
		pre(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
