import os
import glob
import sys
import re

def PreTokenization(tempdatapath, foldertype):
    tokpath = os.path.join(tempdatapath, foldertype + "_tokenizer")
    newtextpath = os.path.join(tempdatapath, foldertype + "_newtext")
    if not os.path.exists(newtextpath): os.makedirs(newtextpath)
    os.chdir(tokpath)
    files = glob.glob('*.tok')
    for file in files:
        f = open(file, 'r')
        fnew = open(os.path.join(newtextpath, file + ".newtext"), 'w')
        line = f.readline()
        while(line != ''):
            p = re.compile(r'[^\s]')
            index = p.findall(line)
            if len(index) == 0:
                line = f.readline()
                continue
            #p10 = re.compile(r'\d{2}/\d{2}/\d{4}') ## do not need to split
            #p6 = re.compile(r'\d{1}-year-old') ## no instance
            #p4 = re.compile(r'\d{2}[A-Za-z]') ## do not need to split
            #p12 = re.compile(r'[A-Z]\d{5}') ## do not need to split
            #p13 = re.compile(r'[a-z]+[A-Z]') ## too strong

            # DATE
            p3 = re.compile(r'[A-Za-z]\d/\d{2}') # DATE
            #p10 = re.compile(r'[A-Z][a-z]+\d{2}\d+') # DATE and other
            p15 = re.compile(r'\d{2}/\d{2}/\d{4}') # DATE
            #p15 = re.compile(r'\d{2}/\d{2}[A-Za-z]')
            #p6 = re.compile(r'\d{2}/\d{2}/\d{4}') # DATE
            #p4 = re.compile(r'\d/\d{2}/\d{4}[A-Za-z]+')

            # AGE
            #p1 = re.compile(r'\d{2}yo') # AGE
            #p5 = re.compile(r'\dyo') # AGE
            p2 = re.compile(r'\d-year-old') # AGE

            # PHONE
            p7 = re.compile(r'[a-z]\d{5}') # PHONE
            p11 = re.compile(r'[A-Z]\d-\d{4}') # PHONE
            p16 = re.compile(r'\d{3}[\- ,]\d{3}[\- ,]\d{4}') # PHONE
            #p16 = re.compile(r'\(\d{3}\) \d{3}-\d{4}') # PHONE


            #p8 = re.compile(r'[A-Z][a-z][a-z]+[A-Z][a-z]+') # LOCATION ?
            p9 = re.compile(r'[A-Z]{2}[a-z][a-z]+') # ?
            
            
            p14 = re.compile(r'\d[A-Za-z][A-Za-z]+') # many types
            
            p18 = re.compile(r'[A-Za-z][a-z]+\d')

            p13 = re.compile(r'[a-z][a-z]+[A-Z]') ## too strong +a little
            
            #index10 = p10.findall(line)
            #index1 = p1.findall(line)
            #index5 = p5.findall(line)
            index2 = p2.findall(line)
            #index6 = p6.findall(line)
            index3 = p3.findall(line)
            #index4 = p4.findall(line)
            index7 = p7.findall(line)
            #index8 = p8.findall(line)
            index9 = p9.findall(line)
            index11 = p11.findall(line)
            #index12 = p12.findall(line)
            index13 = p13.findall(line)
            index14 = p14.findall(line)
            index15 = p15.findall(line)
            index16 = p16.findall(line)
            index18 = p18.findall(line)

            if len(index15) != 0:
                start = 0
                for i in range(len(index15)):
                    #print index15[i]
                    beg = line.find(index15[i],start)
                    if beg == -1: continue
                    end = beg + len(index15[i])
                    #cc = re.findall(r'\d', index15[i])
                    #print cc
                    #cindex = index15[i].find(cc[0])
                    #print index15[i]
                    #print file
                    #print line[beg: end + 5]
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end], ' ' + line[beg:end] + ' ')
                    #print line[beg:beg+cindex] + ' ' + line[beg+cindex:end]
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1

            if len(index3) != 0:
                start = 0
                for i in range(len(index3)):
                    beg = line.find(index3[i],start)
                    if beg == -1: continue
                    end = beg + len(index3[i])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+1] + ' ' + line[beg+1:end])
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1
            '''
            if len(index10) != 0:
                start = 0
                for i in range(len(index10)):
                    beg = line.find(index10[i],start)
                    if beg == -1: continue
                    end = beg + len(index10[i])
                    cc = re.findall(r'\d', index10[i])
                    cindex = index10[i].find(cc[0])
                    print file
                    print line[beg: end + 5]
                    line = line.replace(line[beg:end], line[beg:beg+cindex] + ' ' + line[beg+cindex:end])
                    print line[beg: end + 5]
                    start = end + 1
            '''
            '''
            if len(index1) != 0:
                start = 0
                for i in range(len(index1)):
                    beg = line.find(index1[i],start)
                    if beg == -1: continue
                    end = beg + len(index1[i])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+2] + ' ' + line[beg+2:end] + ' ')
                    #print line[beg - 5: end + 5]
                    #print line[beg - 5: end + 5]
                    start = end + 1
                    '''
            '''
            if len(index5) != 0:
                start = 0
                for i in range(len(index5)):
                    beg = line.find(index5[i],start)
                    if beg == -1: continue
                    end = beg + len(index5[i])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+1] + ' ' + line[beg+1:end] + ' ')
                    #print line[beg - 5: end + 5]
                    start = end + 1
            '''
            if len(index2) != 0:
                start = 0
                for i in range(len(index2)):
                    beg = line.find(index2[i],start)
                    if beg == -1: continue
                    end = beg + len(index2[i])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+1] + ' ' + line[beg+1:end] + ' ')
                    #print line[beg - 5: end + 5]
                    start = end + 1
            '''
            if len(index6) != 0:
                start = 0
                for i in range(len(index6)):
                    beg = line.find(index6[i],start)
                    if beg == -1: continue
                    end = beg + len(index6[i])
                    cc = re.findall(r'\d{2}', index6[i])
                    #print cc
                    cindex = index6[i].find(cc[0])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+cindex] + ' ' + line[beg+cindex:end])
                    #print line[beg - 5: end + 5]
                    start = end + 1
            '''
            
            '''
            if len(index4) != 0:
                start = 0
                for i in range(len(index4)):
                    beg = line.find(index4[i],start)
                    if beg == -1: continue
                    end = beg + len(index4[i])
                    cc = re.findall(r'[A-Za-z]', index4[i])
                    cindex = index4[i].find(cc[0])
                    print file
                    print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+cindex] + ' ' + line[beg+cindex:end])
                    print line[beg - 5: end + 5]
                    start = end + 1
            '''
            
            if len(index7) != 0:
                start = 0
                for i in range(len(index7)):
                    beg = line.find(index7[i],start)
                    if beg == -1: continue
                    end = beg + len(index7[i])
                    #print file
                    #print line[beg - 15: end + 15]
                    line = line.replace(line[beg:end],line[beg:beg+1] + ' ' + line[beg+1:end])
                    #count += 1
                    #print line[beg - 15: end + 15]
                    start = end + 1
            
            if len(index11) != 0:
                start = 0
                for i in range(len(index11)):
                    #print index11[i]
                    beg = line.find(index11[i],start)
                    if beg == -1: continue
                    end = beg + len(index11[i])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+1] + ' ' + line[beg+1:end])
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1

            if len(index16) != 0:
                start = 0
                for i in range(len(index16)):
                    #print index16[i]
                    beg = line.find(index16[i],start)
                    if beg == -1: continue
                    end = beg + len(index16[i])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],' ' + line[beg:end] + ' ')
                    #print line[beg:beg+cindex] + ' ' + line[beg+cindex:end]
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1
            '''
            if len(index8) != 0:
                start = 0
                for i in range(len(index8)):
                    #print index8[i]
                    beg = line.find(index8[i],start)
                    if beg == -1: continue
                    end = beg + len(index8[i])
                    cap = re.compile(r'[A-Z]')
                    cc = cap.findall(index8[i])
                    cindex = index8[i].find(cc[1],1)
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+cindex] + ' ' + line[beg+cindex:end])
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1
            '''
            if len(index9) != 0:
                start = 0
                for i in range(len(index9)):
                    #print index9[i]
                    beg = line.find(index9[i],start)
                    if beg == -1: continue
                    end = beg + len(index9[i])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+1] + ' ' + line[beg+1:end])
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1
                    
            
            '''
            if len(index12) != 0:
                start = 0
                for i in range(len(index12)):
                    #print index12[i]
                    beg = line.find(index12[i],start)
                    if beg == -1: continue
                    end = beg + len(index12[i])
                    line = line.replace(line[beg:end],line[beg:beg+1] + ' ' + line[beg+1:end])
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1
            '''
            if len(index14) != 0:
                start = 0
                for i in range(len(index14)):
                    #print index14[i]
                    beg = line.find(index14[i],start)
                    if beg == -1: continue
                    end = beg + len(index14[i])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+1] + ' ' + line[beg+1:end])
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1

            if len(index18) != 0:
                start = 0
                for i in range(len(index18)):
                    #print index13[i]
                    beg = line.find(index18[i],start)
                    if beg == -1: continue
                    end = beg + len(index18[i])
                    cc = re.findall(r'\d', index18[i])
                    cindex = index18[i].find(cc[0])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+cindex] + ' ' + line[beg+cindex:end])
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1

            if len(index13) != 0:
                start = 0
                for i in range(len(index13)):
                    #print index13[i]
                    beg = line.find(index13[i],start)
                    if beg == -1: continue
                    end = beg + len(index13[i])
                    cc = re.findall(r'[A-Z]', index13[i])
                    cindex = index13[i].find(cc[0])
                    #print file
                    #print line[beg - 5: end + 5]
                    line = line.replace(line[beg:end],line[beg:beg+cindex] + ' ' + line[beg+cindex:end])
                    #print line[beg - 5: end + 5]
                    #count += 1
                    start = end + 1

            line = line.replace('"', ' " ')
            line = line.replace('#', ' # ')
            line = line.replace('(', ' ( ')
            line = line.replace(')', ' ) ')
            line = line.replace('*', ' * ')
            line = line.replace(':', ' : ')
            line = line.replace(';', ' ; ')
            line = line.replace('[', ' [ ')
            line = line.replace(']', ' ] ')
            line = line.replace('{', ' { ')
            line = line.replace('}', ' } ')
            line = line.replace(',', ' , ')
            line = line.replace('<', ' < ')
            line = line.replace('>', ' > ')
            #line = line.replace('.', ' . ')
            line = line.replace('/', ' / ')
            line = line.replace('-', ' - ')
            line = line.replace('=', ' = ')
            fnew.write(line)
            line = f.readline()
        fnew.close()
        f.close()
    newtextfile = open(os.path.join(tempdatapath, foldertype + ".tok"), 'w')
    for i in range(100, 401):
        for j in range(1, 6):
            filename = str(i) + "-0" + str(j) + ".xml.txt.sd.tok.newtext"
            fn = os.path.join(newtextpath, filename)
            if not os.path.exists(fn): continue
            fr = open(fn, 'r')
            newtextfile.write(fr.read())
            newtextfile.write('\n')
            fr.close()
    newtextfile.close()

def main():
    root = sys.path[0]
    datapath = os.path.join(root, sys.argv[1])
    foldertype = sys.argv[2]
    tempdatapath = os.path.join(datapath, "tempdata")
    PreTokenization(tempdatapath, foldertype)
    print "Preprocessing2 finished!"

if __name__ == '__main__': main()