#  -*- coding: utf-8  -*-
'''
前向逐步回归算法：
test(trainfile,prefile,outfile,eps,numIt,splittype)eps每次移动的步长，numIt迭代次数
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

def rssError(yArr,yHatArr): 
    return ((yArr-yHatArr)**2).sum()

def regularize(xMat):
    inMat = xMat.copy()
    inMeans = mean(inMat,0)   
    inVar = var(inMat,0)     
    inMat = (inMat - inMeans)/inVar
    return inMat

def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean    
    xMat = regularize(xMat)
    m,n=shape(xMat)
    ws = zeros((n,1)); wsTest = ws.copy(); wsMax = ws.copy()
    for i in range(numIt):
        print ws.T
        lowestError = inf; 
        for j in range(n):
            for sign in [-1,1]:
                wsTest = ws.copy()
                wsTest[j] += eps*sign
                yTest = xMat*wsTest
                rssE = rssError(yMat.A,yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
    return ws.T

def test(trainfile,prefile,outfile,eps,numIt,splittype):
    print "running...."
    xarr,yarr = loadDataSet(trainfile,splittype)
    weight = stageWise(xarr,yarr,eps,numIt)
    fr = open(prefile)
    fw = open(outfile,'a')
    for line in fr.readlines():
        splitdata = line.split(splittype)
        data = []
        for i in range(len(splitdata)):
            data.append(float(splitdata[i]))
        predata = weight*(mat(data).T)
        fw.write(line.strip() + splittype + str(predata[0,0]) + '\n')
    fw.flush()
    fw.close()
    print "end...."
        
if __name__ == "__main__":
	if sys.argv[6] == "\\t":
		test(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),int(sys.argv[5]),"\t")	
	else:	
		test(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),int(sys.argv[5]),sys.argv[6])
