# -*- coding: utf-8 -*-
'''
使用方法：

test(filename,minsup,splittype)minsup代表最小支持度
'''

import sys

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      
        self.children = {} 
    
    def inc(self, numOccur):
        self.count += numOccur
        
    def disp(self, ind=1):
        print '  '*ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet, minSup=1): 
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in headerTable.keys():  
        if headerTable[k] < minSup: 
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0: return None, None 
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] 
    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet: 
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable 

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count) 
    else:   
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(nodeToTest, targetNode):  
    while (nodeToTest.nodeLink != None):    
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode
        
def ascendTree(leafNode, prefixPath): 
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
    
def findPrefixPath(basePat, treeNode): 
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for basePat in bigL:  
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None: #3. mine cond. FP-tree
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def loadDataSet(filename,splittype):
    fr = open(filename)
    data = []
    datas = []
    for line in fr.readlines():
        lines = line.strip().split(splittype)
        for i in range(len(lines)):
            data.append(lines[i])
        datas.append(data)
        data = []
    return datas

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def test(filename,outfile,minsup,splittype):
    print 'running...'
    fw = open(outfile,'a')
    datamat = loadDataSet(filename,splittype)
    initset = createInitSet(datamat)
    mytree,myheader = createTree(initset,minsup)
    freqItems = []
    mineTree(mytree,myheader,minsup,set([]),freqItems)
    print freqItems
    for i in range(len(freqItems)):
        fw.write(str(list(freqItems[i])) + '\n')
    fw.flush()
    fw.close()
    print 'end...'

if __name__ == "__main__":
	if sys.argv[4] == "\\t":
		test(sys.argv[1],sys.argv[2],float(sys.argv[3]),"\t")
	else:
		test(sys.argv[1],sys.argv[2],float(sys.argv[3]),sys.argv[4])
