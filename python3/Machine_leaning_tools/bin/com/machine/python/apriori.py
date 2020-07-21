# -*- coding: utf-8 -*-
'''
使用方法：

test(filename,minsupport,minconf,splittype)minsupport代表最小支持度，mincof代表最小可信度
'''
from numpy import *
import sys

def loadDataSet(filename,splittype):
    fr = open(filename)
    data = []
    datas = []
    for line in fr.readlines():
        lines = line.strip().split(splittype)
        for i in range(len(lines)):
            data.append(int(lines[i]))
        datas.append(data)
        data = []
    return datas

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
                
    C1.sort()
    return map(frozenset, C1)

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k): 
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: 
                retList.append(Lk[i] | Lk[j]) 
    return retList

def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(outfile,L, supportData, minConf=0.7):  
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(outfile,freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(outfile,freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList         

def calcConf( outfile,freqSet, H, supportData, brl,minConf=0.7):
    fw = open(outfile,'a')
    prunedH = [] 
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] 
        if conf >= minConf: 
            print freqSet-conseq,'-->',conseq,'conf:',conf
            fre = str(list(freqSet-conseq)[:])
            con = str(list(conseq)[:])
            fw.write(fre + '------->' + con + 'conf:'+str(conf) + '\n')
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    fw.flush()
    fw.close()
    return prunedH

def rulesFromConseq(outfile,freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)): 
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(outfile,freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):   
            rulesFromConseq(outfile,freqSet, Hmp1, supportData, brl, minConf)
            
def pntRules(ruleList, itemMeaning):
    for ruleTup in ruleList:
        for item in ruleTup[0]:
            print itemMeaning[item]
        print "           -------->"
        for item in ruleTup[1]:
            print itemMeaning[item]
        print "confidence: %f" % ruleTup[2]

def test(filename,outfile,minsupport,minconf,splittype):
    print "running......"
    datamat = loadDataSet(filename,splittype)
    L,supportdata = apriori(datamat,minsupport)
    rules = generateRules(outfile,L,supportdata,minconf)
    print "end......"

if __name__ == "__main__":
	if sys.argv[5] == "\\t":
		test(sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4]),"\t")	
	else:	
		test(sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4]),sys.argv[5])
