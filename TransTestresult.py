import os
import sys
import re

def dict(category):
    if category=='PATIENT':
        return 'NAME'
    elif category=='DOCTOR':
        return 'NAME'
    elif category=='USERNAME':
        return 'NAME'
    elif category=='PROFESSION':
        return 'PROFESSION'
    elif category=='HOSPITAL':
        return 'LOCATION'
    elif category=='ORGANIZATION':
        return 'LOCATION'
    elif category=='STREET':
        return 'LOCATION'
    elif category=='CITY':
        return 'LOCATION'
    elif category=='STATE':
        return 'LOCATION'
    elif category=='COUNTRY':
        return 'LOCATION'
    elif category=='ZIP':
        return 'LOCATION'
    elif category=='OTHER':
        return 'LOCATION'
    elif category=='AGE':
        return 'AGE'
    elif category=='DATE':
        return 'DATE'
    elif category=='PHONE':
        return 'CONTACT'
    elif category=='FAX':
        return 'CONTACT'
    elif category=='EMAIL':
        return 'CONTACT'
    elif category=='URL':
        return 'CONTACT'
    elif category=='IPADDR':
        return 'CONTACT'
    else:
        return 'ID'

def Makefile(file, testresultfolder, testing_resultpath):
    testresultfilename = os.path.join(testresultfolder, file + ".testresult")
    newfile = os.path.join(testing_resultpath, file)
    testresult_fr = open(testresultfilename, 'r')
    test_fr = open(file, 'r')
    newfile_fw = open(newfile,'w')

    tags_content = []
    tags_sub_type = []
    final_tag = []
    final_st = []
    final_en = []
    final_type = []
    final_text = []
    final_type = []

    patern = re.compile(r'(?<=<!\[CDATA\[)[\s\S]*?(?=\]\]></TEXT>)')
    for each in patern.findall(test_fr.read()):
        eachpiece = each
        break
    textBackup = eachpiece
    line = testresult_fr.readline()
    cut_length = 0
    st_Entity = 0
    en_Entity = 0
    while(1):
        if line == '': break
        if len(line) < 3:
            line = testresult_fr.readline()
            continue
        words = line.split()
        if words[len(words)-1][0]=='B':
            st_Here = eachpiece.find(words[0])
            en_Here = st_Here + len(words[0])
            st_Entity = st_Here + cut_length
            en_Entity = en_Here + cut_length
            eachpiece = eachpiece[en_Here : len(eachpiece)]
            cut_length += en_Here
            tags_sub_type.append(words[len(words)-1].split('-')[1].strip())
            while(1):
                line = testresult_fr.readline()
                if line == '' or len(line) < 3: 
                    tags_content.append(textBackup[st_Entity:en_Entity])
                    final_st.append(st_Entity)
                    final_en.append(en_Entity)
                    break
                words = line.split()
                if words[len(words)-1][0] != 'I': 
                    tags_content.append(textBackup[st_Entity:en_Entity])
                    final_st.append(st_Entity)
                    final_en.append(en_Entity)
                    break
                en_Here = eachpiece.find(words[0]) + len(words[0])
                en_Entity = en_Here + cut_length
                eachpiece = eachpiece[en_Here:len(eachpiece)]
                cut_length += en_Here 
        if words[len(words)-1] == 'O':
            en_Here = eachpiece.find(words[0]) + len(words[0])
            eachpiece = eachpiece[en_Here : len(eachpiece)]
            cut_length += en_Here
            line = testresult_fr.readline()
    eachpiece = textBackup
    newfile_fw.write('<?xml version="1.0" encoding="UTF-8" ?>\n<deIdi2b2>\n<TEXT><![CDATA[')
    newfile_fw.write(eachpiece)
    newfile_fw.write(']]></TEXT>\n<TAGS>\n')
    cut_length = 0  #this val record the length of the cut part, add into position!
    for i in range (0,len(tags_content)):
        if tags_content[i].count('&') != 0: 
            #count += 1
            continue
        final_type.append(tags_sub_type[i])
        final_tag.append(dict(tags_sub_type[i]))
        final_text.append(tags_content[i])
    for i in range(0,len(final_text)):
        strr = '<'
        strr += final_tag[i]
        strr += ' id=\"P'
        strr += str(i)
        strr += '\" start=\"'
        strr += str(final_st[i])
        strr += '\" end=\"'
        strr += str(final_en[i])
        strr += '\" text=\"'
        strr += final_text[i]
        strr += '\" TYPE=\"'
        strr += final_type[i]
        strr += '\" comment=\"\" />\n'
        newfile_fw.write(strr)
    newfile_fw.write('</TAGS>\n</deIdi2b2>')
    newfile_fw.close()
    testresult_fr.close()
    test_fr.close()

def MakeTestingresultfile(testdatapath, testresultfolder, testing_resultpath):
    os.chdir(testdatapath)
    for i in range(100,401):
            for j in range(1,6):
                file = str(i) + '-0' + str(j) + '.xml'
                if not os.path.exists(file): continue
                Makefile(file, testresultfolder, testing_resultpath)
    print "Testing result file generated!"

def GenerateResultfile(testdata, testresultnew, testdatapath, testresultfolder):
    ftest = open(testdata, 'r')
    fnew = open(testresultnew, 'r')
    testdataString = ftest.read()
    ftest.close()
    testfiles = testdataString.split("\n\n\n")
    k = 0
    os.chdir(testdatapath)
    for i in range(100,401):
        for j in range(1,6):
            file = str(i) + '-0' + str(j) + '.xml'
            if not os.path.exists(file): continue
            testresultfile = open(os.path.join(testresultfolder, file + ".testresult"), 'w')
            linenumber = testfiles[k].count('\n') + 1
            k += 1
            for t in range(linenumber):
                testresultfile.write(fnew.readline())
            fnew.readline()
            testresultfile.close()
    fnew.close()

def TagErrorProcess(testresult, testresultnew):
    fnew = open(testresultnew, 'w')
    f = open(testresult, 'r')
    lines = f.readlines()
    num = len(lines)
    i = 0
    count = 0
    lastline = ''
    while i < num:
        if i == 0:
            if lines[i].split()[-1][0] == 'I':
                length = len(lines[i].split()[-1])
                index = - length - 1
                lastline = lines[i][0:index] + 'B' + lines[i][index+1:]
                fnew.write(lastline)
                i += 1
                count += 1
                print i
                continue
            else:
                lastline = lines[i]
                fnew.write(lastline)
                i += 1
                continue
        if lines[i] == '\n':
            lastline = lines[i]
            fnew.write(lastline)
            i += 1
            continue
        if lines[i].split()[-1][0] == 'O':
            lastline = lines[i]
            fnew.write(lastline)
            i += 1
            continue
        if lines[i].split()[-1][0] == 'B':
            lastline = lines[i]
            fnew.write(lastline)
            i += 1
            continue
        if lines[i].split()[-1][0] == 'I':
            if lastline == '\n' or lastline.split()[-1][0] == 'O':
                length = len(lines[i].split()[-1])
                index = - length - 1
                lastline = lines[i][0:index] + 'B' + lines[i][index+1:]
                fnew.write(lastline)
                i += 1
                count += 1
                print i
                continue
            if lastline.split()[-1][0] == 'B' or lastline.split()[-1][0] == 'I':
                if lastline.split()[-1][2:] == lines[i].split()[-1][2:]:
                    lastline = lines[i]
                    fnew.write(lastline)
                    i += 1
                    continue
                else:
                    length = len(lines[i].split()[-1])
                    index = - length - 1
                    lastline = lines[i][0:index] + 'B' + lines[i][index+1:]
                    fnew.write(lastline)
                    i += 1
                    count += 1
                    print i
                    continue
    print 'Error number: ' + str(count)
    print 'Tag error process finished!'

def main():
    root = sys.path[0]
    expfolderpath = os.path.join(root, sys.argv[1])
    datapath = os.path.join(root, sys.argv[2])
    testresult = os.path.join(expfolderpath, sys.argv[3])
    testing_resultpath = os.path.join(expfolderpath, sys.argv[4])
    if not os.path.exists(testing_resultpath): os.makedirs(testing_resultpath)
    testdatapath = os.path.join(datapath, "test")
    tempdatapath = os.path.join(datapath, "tempdata")
    testresultfolder = os.path.join(tempdatapath, "test_result")
    if not os.path.exists(testresultfolder): os.makedirs(testresultfolder)
    testresultnew = testresult + ".new"
    testdata = os.path.join(expfolderpath, sys.argv[5])
    TagErrorProcess(testresult, testresultnew)
    GenerateResultfile(testdata, testresultnew, testdatapath, testresultfolder)
    MakeTestingresultfile(testdatapath, testresultfolder, testing_resultpath)

if __name__ == '__main__': main()
