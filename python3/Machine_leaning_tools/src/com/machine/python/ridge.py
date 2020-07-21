# -*- coding:utf-8 -*-
'''
岭回归使用方法：
test(trainfile,prefile,outfile,num,lamnum,splittype)num代表迭代次数，lam步长的个数
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

def ridgeRegres(xMat,yMat,lam=0.2):
    xTx = xMat.T*xMat
    denom = xTx + eye(shape(xMat)[1])*lam
    if linalg.det(denom) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = denom.I * (xMat.T*yMat)
    return ws
    
def ridgeTest(xArr,yArr,lam):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean 
    xMeans = mean(xMat,0)  
    xVar = var(xMat,0)
    xMat = (xMat - xMeans)/xVar
    numTestPts = lam
    wMat = zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat

def crossValidation(xArr,yArr,numVal,lam):
    m = len(yArr)                           
    indexList = range(m)
    errorMat = zeros((numVal,lam))
    for i in range(numVal):
        trainX=[]; trainY=[]
        testX = []; testY = []
        random.shuffle(indexList)
        if m == 1:
            trainX.append(xArr[indexList[0]])
            trainY.append(yArr[indexList[0]])
            testX.append(xArr[indexList[0]])
            testY.append(yArr[indexList[0]])
        else:
            for j in range(m):
                print '>',
                if j < m*0.9-1: 
                    trainX.append(xArr[indexList[j]])
                    trainY.append(yArr[indexList[j]])
                else:
                    testX.append(xArr[indexList[j]])
                    testY.append(yArr[indexList[j]])
        wMat = ridgeTest(trainX,trainY,lam)  
        for k in range(lam):
            matTestX = mat(testX); matTrainX=mat(trainX)
            meanTrain = mean(matTrainX,0)
            varTrain = var(matTrainX,0)
            matTestX = (matTestX-meanTrain)/varTrain 
            yEst = matTestX * mat(wMat[k,:]).T + mean(trainY)
            errorMat[i,k]=rssError(yEst.T.A,array(testY))
    meanErrors = mean(errorMat,0)
    minMean = float(min(meanErrors))
    bestWeights = wMat[nonzero(meanErrors==minMean)]
    xMat = mat(xArr); yMat=mat(yArr).T
    meanX = mean(xMat,0); varX = var(xMat,0)
    unReg = bestWeights/varX
    print "the best model from Ridge Regression is:\n",unReg
    print "with constant term: ",-1*sum(multiply(meanX,unReg)) + mean(yMat)
    return unReg,-1*sum(multiply(meanX,unReg)) + mean(yMat)

def test(trainfile,prefile,outfile,num,lam,splittype):
    print 'running',
    lgx,lgy = loadDataSet(trainfile,splittype)
    weight,d = crossValidation(lgx,lgy,num,lam)
    fr = open(prefile)
    fw = open(outfile,'a')
    alldata = []
    for line in fr.readlines():
        data = line.strip().split(splittype)
        datas = []
        for i in range(len(data)):
            datas.append(float(data[i]))
        predata = d + weight*(mat(datas).T)
        dat = predata.tolist()
        fw.write(line.strip() +splittype + str(dat[0][0]) + '\n')
    fw.flush()
    fw.close()
    print 'end...'
    

if __name__ == "__main__":
	if sys.argv[6] == "\\t":
		test(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),"\t")
	else:
		test(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),sys.argv[6])
    
