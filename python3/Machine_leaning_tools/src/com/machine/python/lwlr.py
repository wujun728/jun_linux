# -*- coding: utf-8 -*-
'''
局部加权线性回归：
test(trainfilename,prefilename,outfilename,k,splittype)k代表权重衰减程度
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

def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat = mat(xArr); yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):
        print '>',
        diffMat = testPoint - xMat[j,:]     
        weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws

def lwlrTest(testArr,xArr,yArr,k=1.0):  
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i],xArr,yArr,k)
    return yHat

def test(trainfilename,prefilename,outfilename,k,splittype):
    print 'running',
    xarr,yarr = loadDataSet(trainfilename,splittype)
    fr = open(prefilename)
    data = []
    for line in fr.readlines():
        linearr = []
        curline = line.strip().split(splittype)
        for i in range(len(curline)):
            linearr.append(float(curline[i]))
        data.append(linearr)
    fr.close()
    yhat = lwlrTest(data,xarr,yarr,k)
    fw = open(outfilename,'a')
    fr = open(prefilename)
    n = 0
    for line in fr.readlines():
        fw.write(line.strip() + splittype + str(yhat[n]) + '\n')
        n += 1
    fw.flush()
    fw.close()
    print 'END....'

if __name__ == "__main__":
	if sys.argv[5] == "\\t":
		test(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),"\t")	
	else:	
		test(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),sys.argv[5])
