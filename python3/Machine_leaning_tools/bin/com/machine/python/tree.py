# -*- coding: utf-8 -*-
'''
使用方法：
train(trainfile,modelfile,splittype)训练模型，trainfile训练数据，modelfile模型存放文件，splittype数据分割标示符
pre(trainfile,prefile,outfile,modelfile,splittype)预测数据，
'''
from math import log
import operator
import sys

def createDataSet(filename,splittype):
    fr= open(filename)
    dataSet = [inst.strip().split(splittype) for inst in fr.readlines()]
    dataSet.reverse()
    labels = dataSet.pop()
    return dataSet, labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet: 
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2) 
    return shannonEnt
    
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
    
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    print dataSet
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):       
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)      
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)     
        infoGain = baseEntropy - newEntropy     
        if (infoGain > bestInfoGain):       
            bestInfoGain = infoGain       
            bestFeature = i
    return bestFeature                     

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): 
        return classList[0]
    if len(dataSet[0]) == 1: 
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    print bestFeat,labels
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
    return myTree                            
    
def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    print firstStr,inputTree
    featIndex = featLabels.index(firstStr)
    print firstStr,inputTree
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel

def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()
    
def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def train(filename,treefile,splittype):
    print "running...."
    dataSet,labels = createDataSet(filename,splittype)
    print 'createtree.......\n'
    mytree = createTree(dataSet,labels)
    print 'storetree......\n'
    storeTree(mytree,treefile)
    print 'OVER'
def pre(trainfile,prefile,outfile,treefile,splittype):
    print "running...."
    dataSet,labels = createDataSet(trainfile,splittype)
    print labels
    mytree = grabTree(treefile)
    fr= open(prefile)
    fw = open(outfile,'a')
    data = [inst.strip().split(splittype) for inst in fr.readlines()]
    for i in range(len(data)):
        classlabel = classify(mytree,labels,data[i])
        for n in range(len(data[i])):
            fw.write(data[i][n] + splittype)
        fw.write(classlabel + '\n')
        fw.flush()
    fw.close()
    print "end...."

if __name__ == "__main__":
	if len(sys.argv) == 4:
		if sys.argv[3] == "\\t":
			train(sys.argv[1],sys.argv[2],"\t")
		else:
			train(sys.argv[1],sys.argv[2],sys.argv[3])
	elif len(sys.argv) == 6:
		if sys.argv[5] == "\\t":
			pre(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],"\t")
		else:
			pre(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
