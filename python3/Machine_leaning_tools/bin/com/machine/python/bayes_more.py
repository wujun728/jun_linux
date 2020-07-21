# -*- coding: utf-8 -*-
'''
这是一个关于贝叶斯的多分类问题
使用方法如下：
首先将训练数据切分成如loadataet（）函数中的数据形式，预测数据同样也要这种形式。
接着用testingNB()函数进行
'''

from numpy import *
import os
import re
import shutil
import sys

map = {}
def textParse(filepath):    
    bigString = open(filepath).read()
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens] 

def loadDataSet(filespath):
    postingList=[]
    classVec = []    
    filedirs = os.listdir(filespath)
    n = -1
    for fil in filedirs:
        n = n + 1
        map[n] = fil
        files = os.listdir(filespath + '/' + fil)
        for fi in files:
            classVec.append(n)
            wordlist = textParse(filespath + '/' + fil + '/' + fi)
            postingList.append(wordlist)
    return postingList,classVec

def spamTest(filepath):
    docList=[]; classList = []; fullText =[]
    filedirs = os.listdir(filepath)
    n = -1
    for fil in filedirs:
        n = n + 1
        map[n] = fil
        files = os.listdir(filepath + '/' + fil)
        for fi in files:
            wordlist = textParse(filepath + '/' + fil + '/' + fi)
            docList.append(wordlist)
            fullText.extend(wordlist)
            classList.append(n)
    vocabList = createVocabList(docList)
    trainingSet = range(50); testSet=[]           
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    Vect,labeldis = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),Vect,labeldis) != classList[docIndex]:
            errorCount += 1
            print "classification error",docList[docIndex]
    print 'the error rate is: ',float(errorCount)/len(testSet)
    print errorCount,testSet
                 
def createVocabList(dataSet):
    vocabSet = set([])  
    for document in dataSet:
        vocabSet = vocabSet | set(document) 
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    labeldis = {}
    labelnum = {}
    Num = {}
    Denom = {}
    Vect = {}
    for n in range(len(trainCategory)):
        if trainCategory[n] not in labelnum.keys():
            labelnum[trainCategory[n]] = 1
        labelnum[trainCategory[n]] += 1
    lennum = len(labelnum)
    label = labelnum.keys()
    for i in range(lennum):
        labeldis[label[i]] = labelnum[label[i]]/float(numTrainDocs)
        Num[label[i]] = ones(numWords)
        Denom[label[i]] = 2.0                      
    for i in range(numTrainDocs):
        for n in range(lennum):
            if trainCategory[i] == label[n]:
                Num[label[n]] += trainMatrix[n]
                Denom[label[n]] += sum(trainMatrix[n])
    for i in range(lennum):
        Vect[label[i]] = log(Num[label[i]]/Denom[label[i]])         
    return Vect,labeldis

def classifyNB(vec2Classify, Vect, labeldis):
    val = 0.0
    result = ''
    label = Vect.keys()
    for i in range(len(Vect)):
        p = (sum(vec2Classify * Vect[label[i]]) + log(labeldis[label[i]]))
        if p > val or i == 0:
            val = p
            result = str(label[i])
    return result
    
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def testingNB(trainfile,testfile,resultfile):
    print "running...."
    listOPosts,listClasses = loadDataSet(trainfile)
    for n in listClasses:
        if not os.path.exists(resultfile + '/' + map[n]):
            os.mkdir(resultfile + '/' + map[n])
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    Vect,labeldis = trainNB0(array(trainMat),array(listClasses))
    postingList=[]   
    filedirs = os.listdir(testfile)
    for fil in filedirs:
        wordlist = textParse(testfile + '/' + fil)
        postingList.append(wordlist)
        thisDoc = array(setOfWords2Vec(myVocabList, wordlist))
        n = int(classifyNB(thisDoc,Vect,labeldis))
        shutil.move(testfile + '/' + fil,resultfile + '/' + map[n])
        print wordlist,'classified as: ',classifyNB(thisDoc,Vect,labeldis)
    print "end...."

if __name__=="__main__":
	testingNB(sys.argv[1],sys.argv[2],sys.argv[3])
