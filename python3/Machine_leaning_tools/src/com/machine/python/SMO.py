'''
Created on Nov 4, 2010
Chapter 5 source file for Machine Learing in Action
@author: Peter
'''
from numpy import *
from time import sleep
import sys

def loadDataSet(fileName,splittype):
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        data = []
        lineArr = line.strip().split(splittype)
        for i in range(len(lineArr)-1):
            data.append(float(lineArr[i]))
        dataMat.append(data)
        labelMat.append(float(lineArr[-1]))
    return dataMat,labelMat

def selectJrand(i,m):
    j=i #we want to select any J not equal to i
    while (j==i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj > H: 
        aj = H
    if L > aj:
        aj = L
    return aj

def kernelTrans(X, A, kTup): 
    m,n = shape(X)
    K = mat(zeros((m,1)))
    if kTup[0]=='lin': K = X * A.T   
    elif kTup[0]=='rbf':
        for j in range(m):
            deltaRow = X[j,:] - A
            K[j] = deltaRow*deltaRow.T
        K = exp(K/(-1*kTup[1]**2))
    else: raise NameError('Houston We Have a Problem -- \
    That Kernel is not recognized')
    return K
                          
class optStruct:
    def __init__(self,dataMatIn, classLabels, C, toler):  
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((self.m,1)))
        self.b = 0
        self.eCache = mat(zeros((self.m,2)))
        
def calcEk(oS, k):
    fXk = float(multiply(oS.alphas,oS.labelMat).T*(oS.X*oS.X[k,:].T)) + oS.b
    Ek = fXk - float(oS.labelMat[k])
    return Ek
        
def selectJ(i, oS, Ei):         
    maxK = -1; maxDeltaE = 0; Ej = 0
    oS.eCache[i] = [1,Ei]  
    validEcacheList = nonzero(oS.eCache[:,0].A)[0]
    if (len(validEcacheList)) > 1:
        for k in validEcacheList:   
            if k == i: continue 
            Ek = calcEk(oS, k)
            deltaE = abs(Ei - Ek)
            if (deltaE > maxDeltaE):
                maxK = k; maxDeltaE = deltaE; Ej = Ek
        return maxK, Ej
    else:  
        j = selectJrand(i, oS.m)
        Ej = calcEk(oS, j)
    return j, Ej

def updateEk(oS, k):
    Ek = calcEk(oS, k)
    oS.eCache[k] = [1,Ek]
        
def innerL(i, oS):
    Ei = calcEk(oS, i)
    if ((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i]*Ei > oS.tol) and (oS.alphas[i] > 0)):
        j,Ej = selectJ(i, oS, Ei) 
        alphaIold = oS.alphas[i].copy(); alphaJold = oS.alphas[j].copy();
        if (oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = min(oS.C, oS.alphas[j] + oS.alphas[i])
        if L==H: print "L==H"; return 0
        eta = 2.0 * oS.X[i,:]*oS.X[j,:].T - oS.X[i,:]*oS.X[i,:].T - oS.X[j,:]*oS.X[j,:].T
        if eta >= 0: print "eta>=0"; return 0
        oS.alphas[j] -= oS.labelMat[j]*(Ei - Ej)/eta
        oS.alphas[j] = clipAlpha(oS.alphas[j],H,L)
        updateEk(oS, j) 
        if (abs(oS.alphas[j] - alphaJold) < 0.00001): print "j not moving enough"; return 0
        oS.alphas[i] += oS.labelMat[j]*oS.labelMat[i]*(alphaJold - oS.alphas[j])
        updateEk(oS, i) 
        b1 = oS.b - Ei- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.X[i,:]*oS.X[i,:].T - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.X[i,:]*oS.X[j,:].T
        b2 = oS.b - Ej- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.X[i,:]*oS.X[j,:].T - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.X[j,:]*oS.X[j,:].T
        if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]): oS.b = b1
        elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]): oS.b = b2
        else: oS.b = (b1 + b2)/2.0
        return 1
    else: return 0

def smoP(dataMatIn, classLabels, C, toler, maxIter):   
    oS = optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler)
    iter = 0
    entireSet = True; alphaPairsChanged = 0
    while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        alphaPairsChanged = 0
        if entireSet:  
            for i in range(oS.m):        
                alphaPairsChanged += innerL(i,oS)
                print "fullSet, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
            iter += 1
        else:
            nonBoundIs = nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i,oS)
                print "non-bound, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
            iter += 1
        if entireSet: entireSet = False
        elif (alphaPairsChanged == 0): entireSet = True  
        print "iteration number: %d" % iter
    return oS.b,oS.alphas

def calcWs(alphas,dataArr,classLabels):
    X = mat(dataArr); labelMat = mat(classLabels).transpose()
    m,n = shape(X)
    w = zeros((n,1))
    for i in range(m):
        w += multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w

def testRbf(trainfile,C,toler,maxIter,splittype):
    dataArr,labelArr = loadDataSet(trainfile,splittype)
    b,alphas = smoP(dataArr, labelArr, C, toler, maxIter)
    w = calcWs(alphas,dataArr,labelArr)
    datMat=mat(dataArr)
    m,n = shape(datMat)
    errorCount = 0
    for i in range(m):
        predict=datMat[i] * mat(w) + b
        print predict
        if sign(predict)!=sign(labelArr[i]): errorCount += 1
    print "the training error rate is: %f" % (float(errorCount)/m)


def test(trainfile,C,toler,maxIter,splittype):
    print "running..."
    testRbf(trainfile,C,toler,maxIter,splittype)
    print "end..."

def pre(trainfile,prefile,outfile,C,toler,maxIter,splittype):
    print "running...."
    fw = open(outfile,'a')
    dataArr,labelArr = loadDataSet(trainfile,splittype)
    b,alphas = smoP(dataArr, labelArr, C, toler, maxIter)
    w = calcWs(alphas,dataArr,labelArr)
    datMat=mat(dataArr)
    dataMat = []
    fr = open(prefile)
    for line in fr.readlines():
        data = []
        lineArr = line.strip().split(splittype)
        for i in range(len(lineArr)):
            data.append(float(lineArr[i]))
        predict=mat(data) * mat(w) + b
        da = predict.tolist()
        if da[0][0] < 0:
            dd = -1.0
        else:
            dd = 1.0
        fw.write(line.strip() + splittype + str(dd) + '\n')
    fw.flush()
    fw.close()
    fr.close()
    print 'end......'

if __name__ == "__main__":
	if len(sys.argv) == 6:
		if sys.argv[5] == "\\t":
			test(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),"\t")
		else:
			test(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),sys.argv[5])
	elif len(sys.argv) == 8:
		if sys.argv[7] == "\\t":
			pre(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),"\t")
		else:
			pre(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),sys.argv[7])
