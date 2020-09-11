import math as m
import numpy as np
import random as r
import sys
import dataloader
import features

#"B-LOC","B-MISC","B-ORG","B-PER",
potentialTags = {"I-LOC","I-MISC","I-ORG","I-PER","O"}

def main():
    # get training and test data
    print("Importing training data")
    trainD = dataloader.getTrainingData()
    trainL = dataloader.getTrainingLabels()
    print("Importing test data")
    devD = dataloader.getDevData()
    devL = dataloader.getDevLabels()
    # create random weights between 0 and 1
    f = initializeFeatureVector()
    w = initializeWeights(f.fv)
    # get word counts
    initCounts(trainD, trainL, f)
    # train
    print("Training")
    epochs = 7
    test(devD, devL, w, f.fv)
    wavg = train(trainD, trainL, epochs, w, f.fv, devD, devL)
    # generate the output using the test data
    testD = dataloader.getTestData()
    testL = dataloader.getTestLabels()
    createOutput(testD, testL, wavg, f.fv, "output.txt")
    createOutput(devD, devL, wavg, f.fv, "output-dev.txt")

def createOutput(testD, testL, w, fv, filename):
    for i in range(len(testD)):
        predicted = getResult(testD[i], w, fv)
        for j in range(len(predicted)):
            testD[i][j] = np.append(np.append(testD[i][j], testL[i][j]), predicted[j])
    dataloader.output(filename, testD)
    
def test(testD, testL, w, fv):
    correct = 0
    total = 0
    print(w)
    for i in range(len(testD)):
        predicted = getResult(testD[i], w, fv)
        for k in range(len(predicted)):
            total += 1
            if predicted[k] == testL[i][k]:
                correct += 1
    print('accuracy: ' + str(100*(correct/total)) + ' %')

def train(trainD, trainL, epochs, w, fv, testD, testL):
    wavg = np.zeros(len(w))
    for epoch in range(epochs):
        print('*** epoch ' + str(epoch) + ' ***')
        for i in range(len(trainD)):
            predicted = getResult(trainD[i], w, fv)
            expected = trainL[i]
            predictedFV = getFeatureVals(predicted, trainD[i], fv)
            expectedFV = getFeatureVals(expected, trainD[i], fv)
            w = adjustWeights(w, getErr(predictedFV, expectedFV))
            wavg = wavg + (w/len(trainD))
        # test after every epoch
        test(testD, testL, wavg, fv)
    return wavg
    
def getErr(predicted, expected):
    return expected - predicted

def adjustWeights(w, err):
    return w + err

def getFeatureVals(tags, sentence, fv):
    fVals = []
    for fi in range(len(fv)):
        fRes = 0
        for i in range(len(sentence)):
            prevTag = '_START_'
            fRes = fRes + (fv[fi](sentence, i, prevTag, tags[i]))
        fVals.append(fRes)
    return np.array(fVals)

def getResult(sentence, w, fv):
    # find best tag sequence for the sentence
    modSentence = []
    modSentence.append(['_START_','_START_','_START_','_START_'])
    modSentence.extend(sentence)
    tags = []
    iMap = {}
    bpMap = {}
    iMap[0] = {}
    for t in potentialTags:
        iMap[0][t] = 0
    iMap[0]['_START_'] = 1
    for i in range(1, len(modSentence)):
        iMap[i] = {}
        bpMap[i] = {}
        for tag in potentialTags:
            maxProb = -sys.float_info.max
            maxTag = ''
            for prevTag in potentialTags:
                prob = calculate(modSentence, tag, prevTag, i, w, fv)
                if prob > maxProb:
                    maxProb = prob
                    maxTag = prevTag
            iMap[i][tag] = maxProb
            bpMap[i][tag] = maxTag

    maxLast = -sys.float_info.max
    maxTag = ''
    lastMap = iMap[len(modSentence) - 1]
    for tag in lastMap:
        if lastMap[tag] > maxLast:
            maxLast = lastMap[tag]
            maxTag = tag
    tags.append(maxTag)
    if len(sentence) == 1:
        return tags
    for i in range(len(modSentence) - 1, 1, -1):
        prev = bpMap[i][maxTag]
        tags.append(prev)
        maxTag = prev
    tags.reverse()
    return tags

def calculate(sentence, tag, prevTag, i, w, fv):
    fRes = []
    for fi in range(len(fv)):
        fRes.append(fv[fi](sentence, i, prevTag, tag))
    return sum(fRes * w)

def initCounts(data, labels, f):
    for l in range(len(data)):
        line = [['_START_','_START_','_START_']]
        line.extend(data[l])
        lineLabels = ['_START_']
        lineLabels.extend(labels[l])
        prevTag = "_START_"
        for w in range(len(line)):
            # word counts
            if line[w][0] in f.wordCount:
                f.wordCount[line[w][0]] = f.wordCount[line[w][0]] + 1
            else:
                f.wordCount[line[w][0]] = 1

            # tag to word count
            if lineLabels[w] not in f.tagWordCount:
                f.tagWordCount[lineLabels[w]] = {}
            if line[w][0] in f.tagWordCount[lineLabels[w]]:
                f.tagWordCount[lineLabels[w]][line[w][0]] = f.tagWordCount[lineLabels[w]][line[w][0]] + 1
            else:
                f.tagWordCount[lineLabels[w]][line[w][0]] = 1

            # tag to pos count
            if lineLabels[w] not in f.tagPosCount:
                f.tagPosCount[lineLabels[w]] = {}
            if line[w][1] in f.tagPosCount[lineLabels[w]]:
                f.tagPosCount[lineLabels[w]][line[w][1]] = f.tagPosCount[lineLabels[w]][line[w][1]] + 1
            else:
                f.tagPosCount[lineLabels[w]][line[w][1]] = 1

            # tag to chunk count
            if lineLabels[w] not in f.tagChunkCount:
                f.tagChunkCount[lineLabels[w]] = {}
            if line[w][2] in f.tagChunkCount[lineLabels[w]]:
                f.tagChunkCount[lineLabels[w]][line[w][2]] = f.tagChunkCount[lineLabels[w]][line[w][2]] + 1
            else:
                f.tagChunkCount[lineLabels[w]][line[w][2]] = 1

            # tag to prevTag count
            if lineLabels[w] not in f.tagTagCount:
                f.tagTagCount[lineLabels[w]] = {}
            if prevTag in f.tagTagCount[lineLabels[w]]:
                f.tagTagCount[lineLabels[w]][prevTag] = f.tagTagCount[lineLabels[w]][prevTag] + 1
            else:
                f.tagTagCount[lineLabels[w]][prevTag] = 1

            # update prevTag
            prevTag = lineLabels[w]

    # add totals
    totalWords = 0
    for word in f.wordCount:
        totalWords += f.wordCount[word]
    f.wordCount["_TOTAL_"] = totalWords
        
    for tag in list(f.tagWordCount):
        total = 0
        for word in f.tagWordCount[tag]:
            total += f.tagWordCount[tag][word]
        f.tagWordCount[tag]["_TOTAL_"] = total
        
    for tag in list(f.tagPosCount):
        total = 0
        for pos in f.tagPosCount[tag]:
            total += f.tagPosCount[tag][pos]
        f.tagPosCount[tag]["_TOTAL_"] = total

    for tag in list(f.tagChunkCount):
        total = 0
        for chunk in f.tagChunkCount[tag]:
            total += f.tagChunkCount[tag][chunk]
        f.tagChunkCount[tag]["_TOTAL_"] = total

    for tag in list(f.tagTagCount):
        total = 0
        for prev in f.tagTagCount[tag]:
            total += f.tagTagCount[tag][prev]
        f.tagTagCount[tag]["_TOTAL_"] = total

def initializeFeatureVector():
    f = features.Features()
    f.fv.append(f.f0)
    f.fv.append(f.f1)
    f.fv.append(f.f2)
    f.fv.append(f.f3)
    f.fv.append(f.f4)
    f.fv.append(f.f5)
    f.fv.append(f.f6)
    f.fv.append(f.f7)
    f.fv.append(f.f8)
    f.fv.append(f.f9)
    f.fv.append(f.f10)
    f.fv.append(f.f11)
    f.fv.append(f.f12)
    f.fv.append(f.f13)
    f.fv.append(f.f14)
    f.fv.append(f.f15)
    f.fv.append(f.f16)
    f.fv.append(f.f17)
    f.fv.append(f.f18)
    f.fv.append(f.f19)
    f.fv.append(f.f20)
    f.fv.append(f.f21)
    f.fv.append(f.f22)
    f.fv.append(f.f23)
    f.fv.append(f.f24)
    f.fv.append(f.f25)
    f.fv.append(f.f26)
    f.fv.append(f.f27)
    f.fv.append(f.f28)
    f.fv.append(f.f29)
    f.fv.append(f.f30)
    return f

def initializeWeights(fv):
    return np.array([r.random() for i in range(len(fv))])

if __name__ == "__main__": main()