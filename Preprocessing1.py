import os
import glob
import sys
import re

def extractText(folderpath, textpath):
    os.chdir(folderpath)
    files = glob.glob('*.xml')
    for file in files:
        filetext = os.path.join(textpath, file + ".txt")
        filetextw = open(filetext, 'w')
        f = open(file, 'r')
        fr = f.read()
        begin = fr.find('CDATA[') + 6
        end = fr.find(']]></TEXT>')
        text1 = fr[begin:end].replace('_', ' ')
        text2 = text1.replace('~', ' ')
        text3 = text2.replace('^', ' ')
        text4 = text3.replace('&', ' ')
        #text5 = text4.replace('\n', ' ')
        text = text4.replace('\t', ' ')
        filetextw.write(text)
        f.close()
        filetextw.close()

def extractTextandTags(folderpath, textpath, tagpath):
    os.chdir(folderpath)
    files = glob.glob("*.xml")
    for file in files:
        f = open(file, 'r')
        fr = f.read()
        begin = fr.find('CDATA[') + 6
        end = fr.find(']]></TEXT>')
        textw1 = fr[begin:end]
        textw2 = textw1.replace('_', ' ')
        textw3 = textw2.replace('~', ' ')
        textw4 = textw3.replace('^', ' ')
        textw5 = textw4.replace('&', ' ')  # need to be considered!
        #text1 = textw.replace('\n', ' ')
        textw = textw5.replace('\t', ' ')
        start = fr.find('<TAGS>') + 6
        finish = fr.find('</TAGS>')
        tags = fr[start:finish]
        list = []
        start = 0
        filene = os.path.join(tagpath, file + ".netag")
        filenew = open(filene, 'w')
        text = textw.replace('\n', ' ')
        #text = text1.replace('\t', ' ')
        while(1):
            index = tags.find('start="', start)
            if index == -1:
                break
            index1 = index + 7
            index2 = tags.find('" end="', start)
            index3 = index2 + 7
            index4 = tags.find('" text="', start)
            index5 = tags.find('TYPE="', start) + 6
            index6 = tags.find('" comment=', start)  
            s1 = int(tags[index1:index2])
            s2 = int(tags[index3:index4])
            type = tags[index5:index6]
            start = index6 + 16
            list.append(([s1,s2],type))
        filetext = os.path.join(textpath, file + ".txt")
        filetextw = open(filetext, 'w')

        for i in range(len(list)):
            # first tag
            if i == 0:
                text0 = text[:list[i][0][0]]
                text0w = text0.split(' ')
                num = text0w.count('')
                for k in range(0,num):
                    text0w.remove('')
                for j in range(len(text0w)):
                    tmp = text0w[j] + ' O\n'
                    filenew.write(tmp)
                filetextw.write(textw[:list[i][0][0]])

            # tag in the middle and last tag
            textphi = text[list[i][0][0]:list[i][0][1]]
            phitype = list[i][1]
            textphiw = textphi.split(' ')
            for j in range(len(textphiw)):
                if j == 0:
                    tmp = textphiw[j] + ' B-' + phitype + '\n'
                    filenew.write(tmp)
                else:
                    tmp = textphiw[j] + ' I-' + phitype + '\n'
                    filenew.write(tmp) 
            filetextw.write(' ' + textw[list[i][0][0]:list[i][0][1]] + ' ')

            # last tag
            if i == len(list) - 1:
                texto = text[list[i][0][1]:len(text)]
                textow = texto.split(' ')
                num = textow.count('')
                for k in range(0,num):
                    textow.remove('')
                for j in range(len(textow)):
                    tmp = textow[j] + ' O\n'
                    filenew.write(tmp)
                filetextw.write(textw[list[i][0][1]:len(text)])
            else:
                # tag in the middle
                texto = text[list[i][0][1]:list[i+1][0][0]]
                textow = texto.split(' ')
                #print textow
                num = textow.count('')
                for k in range(0,num):
                    textow.remove('')
                for j in range(len(textow)):
                    tmp = textow[j] + ' O\n'
                    filenew.write(tmp)
                filetextw.write(textw[list[i][0][1]:list[i+1][0][0]])
        filetextw.close()
        filenew.close()
        f.close()

def TextandTags(datapath, tempdatapath, foldertype):
    folderpath = os.path.join(datapath, foldertype)
    textpath = os.path.join(tempdatapath, foldertype + "_text")
    if not os.path.exists(textpath): os.makedirs(textpath)

    if foldertype == "train":
        tagpath = os.path.join(tempdatapath, foldertype + "_tags")
        if not os.path.exists(tagpath): os.makedirs(tagpath)
        extractTextandTags(folderpath, textpath, tagpath)
    else:
        extractText(folderpath, textpath)

def main():
    root = sys.path[0]
    datapath = os.path.join(root, sys.argv[1])
    foldertype = sys.argv[2]
    tempdatapath = os.path.join(datapath, "tempdata")
    if not os.path.exists(tempdatapath): os.makedirs(tempdatapath)
    TextandTags(datapath, tempdatapath, foldertype)
    print "Preprocessing1 finished!"

if __name__ == '__main__': main()
