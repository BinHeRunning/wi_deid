import os
import sys

# python AddDicFeatures.py dicfolderpath train.data train_dic.data test.data test_dic.data

def AddDicFeaturesToTest(dics, testdata, testdicdata):
    fr = open(testdata, 'r')
    fw = open(testdicdata, 'w')
    line = fr.readline()
    #count = 0
    while line != '':
        if line == '\n':
            fw.write(line)
            line = fr.readline()
            continue
        lineparts = line.split()
        targetword = lineparts[0].lower()
        wordlemma = lineparts[1].lower()
        featurestring = ''
        for key in dics:
            if dics[key].has_key(targetword): featurestring += '\t1'
            else: featurestring += '\t0'
            #if count == 0: print key
        #count = 1
        newline = line.strip() + featurestring + '\t' + targetword + '\t' + wordlemma + '\n'
        fw.write(newline)
        line = fr.readline()
    fr.close()
    fw.close()

def AddDicFeaturesToTrain(dics, traindata, traindicdata):
    fr = open(traindata, 'r')
    fw = open(traindicdata, 'w')
    line = fr.readline()
    #count = 0
    while line != '':
        if line == '\n':
            fw.write(line)
            line = fr.readline()
            continue
        lineparts = line.split()
        targetword = lineparts[0].lower()
        wordlemma = lineparts[1].lower()
        featurestring = ''
        for key in dics:
            if dics[key].has_key(targetword): featurestring += '1\t'
            else: featurestring += '0\t'
            #if count == 0: print key
        #count = 1
        if lineparts[-1] == 'O':
            newline = line[:-2] + featurestring + targetword + '\t' + wordlemma + '\t' + 'O\n'
            fw.write(newline)
            line = fr.readline()
            continue
        index = line.find(lineparts[-1])
        newline = line[:index] + featurestring + targetword + '\t' + wordlemma + '\t' + lineparts[-1] + '\n'
        fw.write(newline)
        line = fr.readline()
    fr.close()
    fw.close()

def ReadDic(dicfolderpath, dictype):
    dic = {}
    for dictypename in dictype:
        dicfilename = dictypename + '.txt'
        dicfile = os.path.join(dicfolderpath, dicfilename)
        subdic = {}
        fr = open(dicfile, 'r')
        line = fr.readline()
        while line != '':
            word = line.strip().split('\t')[0]
            subdic[word] = 1
            line = fr.readline()
        fr.close()
        dic[dictypename] = subdic
    return dic

def main():
    root = sys.path[0]
    dicfolderpath = os.path.join(root, sys.argv[1])
    traindata = os.path.join(root, sys.argv[2])
    traindicdata = os.path.join(root, sys.argv[3])
    testdata = os.path.join(root, sys.argv[4])
    testdicdata = os.path.join(root, sys.argv[5])
    #dictype = ['city', 'country', 'date', 'doctor', 'hospital', 'organization', 'patient', 'profession', 'state', 'street']
    dictype = ['city', 'country', 'date', 'state', 'street']
    # read dicfiles to dic
    dics = ReadDic(dicfolderpath, dictype)
    # add dic features to train data
    AddDicFeaturesToTrain(dics, traindata, traindicdata)
    # add dic features to test data
    AddDicFeaturesToTest(dics, testdata, testdicdata)
    print 'Dic Features Added!'

if __name__ == '__main__':
    main()