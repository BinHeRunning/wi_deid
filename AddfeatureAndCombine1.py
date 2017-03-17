import sys
import glob
import os
import re

def Datatrans(expfolderpath, tempdatapath, foldertype):
    fileFrom = open(os.path.join(tempdatapath, foldertype + ".featured"), 'r')
    fileTo = open(os.path.join(expfolderpath, foldertype + ".data"), 'w')
    fileTo.write(fileFrom.read())
    fileFrom.close()
    fileTo.close()

def CombineFeaturefileAndNefile(fn, fr, fw):
    linenum = 1
    flag = 0
    netagfr = open(fn, 'r')
    netagline = netagfr.readline()
    while(netagline != ''):
        if flag == 1:
            break
        line = netagline.split(' ')
        linetext = line[0]
        linetype = line[1]
        tag = 0
        while(linetext != ''):
            tpcline = fr.readline()
            if tpcline == '':
                break
            if tpcline == '\n':
                fw.write('\n')
                linenum += 1
                continue
            tpctext = tpcline.split('\t')[0]
            len1 = len(tpctext)
            len2 = len(linetext)
            j = len1
            for i in range(len1):
                if i > len2 - 1: 
                    j = i
                    break
                if tpctext[i] == linetext[i] : continue
            if tpctext[j:] != '':
                #print "Error in line:" + str(linenum)
                #print tpctext[j:]
                flag = 1
                break
            linetext = linetext[len(tpctext):]
            combineqian = tpcline.replace('\n','\t')
            if len(linetype) > 2 and tag == 1:
                type = "I-" + linetype[2:]
            else:
                type = linetype
            combinetext = combineqian + type
            fw.write(combinetext)
            linenum += 1
            if linetext != '':
                tag = 1
        netagline = netagfr.readline()
    netagfr.close()

def Tagcombine(expfolderpath, tempdatapath, foldertype, featuredfile):
    tagpath = os.path.join(tempdatapath, foldertype + "_tags")
    combinedfile = os.path.join(expfolderpath, foldertype + ".data")
    fw = open(combinedfile, 'w')
    fr = open(featuredfile, 'r')
    for i in range(100, 401):
        for j in range(1, 6):
            filename = str(i) + "-0" + str(j) + ".xml.netag"
            fn = os.path.join(tagpath, filename)
            if not os.path.exists(fn): continue
            CombineFeaturefileAndNefile(fn, fr, fw)
    fw.write(fr.read())
    fr.close()
    fw.close()

def Num(string):
    flag = 0
    for i in range(len(string)):
        index = string[i].isdigit()
        if index: flag = 1
    return flag

def Cap(string):
    flag = 0
    for i in range(len(string)):
        index = string[i].isupper()
        if index: flag = 1
    return flag

def Feature(file1, file2):
    file1r = open(file1, 'r')
    file2w = open(file2, 'w')
    line = file1r.readline()
    while(line != ''):
        if line == '\n':
            file2w.write('\n')
            line = file1r.readline()
            continue
        linesplit = line.split('\t')
        word = linesplit[0]

        # trans `` to "
        lineqian = line.replace('\n','\t')
        index = word.find("``")
        if index != -1:
            word = word[:index] + '"' + word[index + 2:]
            pattern = re.compile(r'``')
            index = pattern.findall(lineqian)
            for i in range(len(index)):
                begin = lineqian.find('``')
                end = begin + 2
                lineqian = lineqian[:begin] + '"' + lineqian[end:]

        # features
        wordlength = len(word)  # 1 length

        if word.istitle(): ititle = 1  # 2 word first letter is capitalized 
        else: ititle = 0
        icap = Cap(word)  # 3 word contains capitalized letter or not
        pattern1 = re.compile(r'[A-Z]+')
        matches = pattern1.findall(word)
        if len(matches) > 0 and len(matches[0]) == wordlength: allcap = 1  # 4 all capitalized
        else: allcap = 0
        pattern2 = re.compile(r'[A-Za-z]+')
        matches = pattern2.findall(word)
        if len(matches) > 0 and len(matches[0]) > 0: iletter = 1  # 5 word contains letter or not
        else: iletter = 0 

        inum = Num(word)  # 6 word contains number or not
        pattern3 = re.compile(r'\d+')
        matches = pattern3.findall(word)
        if len(matches) > 0 and len(matches[0]) == wordlength: allnum = 1  # 7 all number
        else: allnum = 0

        punc = re.findall('''[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]''', word)
        if len(punc) > 0: ipunc = 1  # 8 word contains punctuation or not
        else: ipunc = 0
        
        if iletter == 1 and inum == 1 and ipunc == 0: iln = 1  # 9 word consisted by letters and numbers
        else: iln = 0

        if iletter == 0 and inum == 1 and ipunc == 1: inp = 1  # 10 word consisted by numbers and punc
        else: inp = 0

        front2 = word[:2]  # 11 first two letters
        last2 = word[-2:]  # 12 last two letters
        front4 = word[:4]  # 13 first four letters
        last4 = word[-4:]  # 14 last four letters
        
        # 15 word shape
        p1 = re.compile(r'[1-9]')  # turn numbers to 0
        index = p1.findall(word)
        for i in range(len(index)):
            begin = word.find(index[i])
            end = begin + 1
            word = word[:begin] + '0' + word[end:] 
        p2 = re.compile(r'[B-Z]')  # cap letters to A
        index = p2.findall(word)
        for i in range(len(index)):
            begin = word.find(index[i])
            end = begin + 1
            word = word[:begin] + 'A' + word[end:]
        p3 = re.compile(r'[b-z]')  # lower letters to a
        index = p3.findall(word)
        for i in range(len(index)):
            begin = word.find(index[i])
            end = begin + 1
            word = word[:begin] + 'a' + word[end:]
        
        # 16 word contains AT or not
        #atindex = word.find('@')
        #if atindex != -1: at = 1
        #else: at = 0

        newline = lineqian + str(wordlength) + '\t' + str(ititle) + '\t' + str(icap) \
        + '\t' + str(allcap) + '\t' + str(iletter) + '\t' + str(inum) + '\t' \
        + str(allnum) + '\t' + str(ipunc) + '\t' + str(iln) + '\t' + str(inp) + '\t' \
        + front2 + '\t' + last2 + '\t' + front4 + '\t' + last4 + '\t' + word + '\n'
        file2w.write(newline)
        line = file1r.readline()
    file1r.close()
    file2w.close()

def main():
    root = sys.path[0]
    datapath = os.path.join(root, sys.argv[1])
    foldertype = sys.argv[2]
    expfolderpath = os.path.join(root, sys.argv[3])
    if not os.path.exists(expfolderpath): os.makedirs(expfolderpath)
    tempdatapath = os.path.join(datapath, "tempdata")
    tpcfile = os.path.join(tempdatapath, foldertype + ".tpc")
    featuredfile = os.path.join(tempdatapath, foldertype + ".featured")
    Feature(tpcfile, featuredfile)
    if foldertype == "train":
        Tagcombine(expfolderpath, tempdatapath, foldertype, featuredfile)
        print foldertype + "ing data generated!"
    else:
        Datatrans(expfolderpath, tempdatapath, foldertype)
        print foldertype + " data generated!"

if __name__ == '__main__': main()