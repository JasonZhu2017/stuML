

import os
import os.path
from numpy import *
import operator

def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistance = sqDiffMat.sum(axis = 1)
    distance = sqDistance ** 0.5
    sortedDistance = distance.argsort()
    classCount = {}
    for i in range(k):
        voteLabel = labels[sortedDistance[i]]
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(),\
                 key = operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    if not os.path.exists(filename):
        print "[error]\tcann't find file: %s" % (filename)
        return None
    with open(filename, "r") as fr:
        fileLines = fr.readlines()
        lineNum = len(fileLines)
        featureMat = zeros((lineNum, 3))
        labelsVector = []
        index = 0
        for line in fileLines:
            line = line.strip()
            items = line.split("\t")
            featureMat[index, :] = items[0 : 3]
            labelsVector.append(int(items[-1]))
            # labelsVector.append(items[-1])
            index += 1
        return featureMat, labelsVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges =  maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges, minVals

def datingCalssTest():
    hoRatio = 0.5
    datingMat, labelVec = file2matrix("datingTestSet2.txt")
    normMat, rangs, minVals = autoNorm(datingMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],\
         normMat[numTestVecs:m, : ], labelVec[numTestVecs:m], 3)
        print "the classifierResult is: %d, the real answer is: %d" \
            % (classifierResult, labelVec[i])
        if (classifierResult != labelVec[i]):
            errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))


def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input("percantage of time spent playing  vedio games?"))
    ffMiles = float(raw_input("frequent flier miles"))
    iceCream = float(raw_input("ice cream consumed"))
    datingMat, labelVec = file2matrix("datingTestSet2.txt")
    normMat, ranges, minVals = autoNorm(datingMat)
    inArray = [percentTats, ffMiles, iceCream]
    classifierRst = classify0((inArray - minVals) / ranges,\
        normMat, labelVec, 3)
    print "You will probably like the person:", resultList[classifierRst - 1]


def img2vector(filename):
    rtnVect =  zeros((1,1024))
    with open(filename) as fh:
        for i in range(32):
            linestr = fh.readline()
            for j in range(32):
                rtnVect[0, 32*i+j] = int(linestr[j])
        return rtnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir("trainingDigits/")
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        filename = trainingFileList[i]
        hwLabels.append(int(filename.split('.')[0].split('_')[0]))
        trainingMat[i, :] = img2vector("trainingDigits/%s" % filename)
    testFileList = os.listdir("testDigits/")
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        filename = testFileList[i]
        classStr = int(filename.split('.')[0].split('_')[0])
        labelsVect = img2vector("testDigits/%s" % filename)
        classRS = classify0(labelsVect, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" \
                    % (classRS, classStr)
        if (classStr != classRS):
            errorCount += 1.0
    print "\nthe total number of error is: %d" % (errorCount)
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))

if __name__ == "__main__":
    # datingCalssTest()
    handwritingClassTest()