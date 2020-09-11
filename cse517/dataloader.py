import numpy as np
import csv

def getTrainingData():
    return getData('conll03_ner/eng.train.small')
    
def getTrainingLabels():
    return getLabels('conll03_ner/eng.train.small')
    
def getDevData():
    return getData('conll03_ner/eng.dev.small')
    
def getDevLabels():
    return getLabels('conll03_ner/eng.dev.small')

def getTestData():
    return getData('conll03_ner/eng.test.small')
    
def getTestLabels():
    return getLabels('conll03_ner/eng.test.small')

def getData(filename):
    f = open(filename, newline='')
    r = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
    data = []
    temprow = []
    for row in r:
        row = np.array(row)
        if len(row) > 0:
            if row[0] == '-DOCSTART-':
                continue
            temprow.append(row[0:3])
        else:
            if len(temprow) > 0:
                data.append(temprow)
            temprow = []
    f.close()
    return data

def getLabels(filename):
    f = open(filename, newline='')
    r = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
    data = []
    temprow = []
    for row in r:
        row = np.array(row)
        if len(row) > 0:
            if row[0] == '-DOCSTART-':
                continue
            temprow.append(row[3])
        else:
            if len(temprow) > 0:
                data.append(temprow)
            temprow = []
    f.close()
    return data

def output(filename, data):
    f = open(filename, 'w')
    w = csv.writer(f, delimiter=' ', quotechar = "'")
    for row in data:
        for word in row:
            w.writerow(word)
    f.close()
