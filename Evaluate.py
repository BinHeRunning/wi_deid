from __future__ import division
import os
import sys
import glob

def match_evaluation(goldpath,testing_resultpath,type):
    ininum = 0
    matchnum = 0
    agreenum = 0
    os.chdir(testing_resultpath)
    mfiles = glob.glob('*.xml')
    for mfile in mfiles:
        #file = mfile
        #print file
        mfr = open(mfile,'r').read()
        fr = open(os.path.join(goldpath, mfile), 'r').read()
        mtag_b = mfr.find('<TAGS>') + 7
        mtag_e = mfr.find('</TAGS>')
        mtags = mfr[mtag_b:mtag_e]
        tag_b = fr.find('<TAGS>') + 7
        tag_e = fr.find('</TAGS>')
        tags = fr[tag_b:tag_e]
        mtag = []
        tag = []
        mstart = 0
        start = 0
        while(1):
            temp_b = mtags.find('start=',mstart)
            type_b = mtags.find('TYPE="',mstart) + 6
            type_e = mtags.find('" comment=',mstart)
            typename = mtags[type_b:type_e]
            if typename == type:
                temp_e = mtags.find('comment=',mstart)
                mtag.append(mtags[temp_b:temp_e])
            mstart = type_e + 16
            if mstart > len(mtags) - 1: break
        while(1):
            temp_b = tags.find('start=',start)
            type_b = tags.find('TYPE="',start) + 6
            type_e = tags.find('" comment=',start)
            typename = tags[type_b:type_e]
            if typename == type:
                temp_e = tags.find('comment=',start)
                tag.append(tags[temp_b:temp_e])
            start = type_e + 16
            if start > len(tags) - 1: break
        ininum += len(tag)
        #print file
        #print ininum
        matchnum += len(mtag)
        for t in tag:
            index = mtag.count(t)
            if index > 0: agreenum += 1
    #print ininum,matchnum,agreenum
    return ininum,matchnum,agreenum

def main():
    root = sys.path[0]
    datapath = os.path.join(root, sys.argv[1])
    expfolderpath = os.path.join(root, sys.argv[2])
    testing_resultpath = os.path.join(expfolderpath, sys.argv[3])
    goldpath = os.path.join(datapath, "testing-PHI-Gold-fixed")
    valid_TYPE = ["PATIENT", "DOCTOR", "USERNAME", "PROFESSION", "HOSPITAL", "ORGANIZATION", \
                "STREET", "CITY", "STATE", "COUNTRY", "ZIP", "OTHER", "LOCATION-OTHER", "AGE", \
                "DATE", "PHONE", "FAX", "EMAIL", "URL", "IPADDR", "SSN", "MEDICALRECORD", \
                "HEALTHPLAN", "ACCOUNT", "LICENSE", "VEHICLE", "DEVICE", "BIOID", "IDNUM"]
    agree = 0
    G = 0
    N = 0
    for type in valid_TYPE:
        ininum,matchnum,agreenum = match_evaluation(goldpath,testing_resultpath,type)
        agree += agreenum
        G += ininum
        N += matchnum
        print (type)
        if ininum == 0:
            print ('Gold:%d,' % ininum)
            print ('New:%d.\n' % matchnum)
        else:
            print ('Gold:%d,' % ininum)
            if matchnum == 0: 
                print ('New:%d.\n' % matchnum)
            else:
                print ('New:%d,' % matchnum)
                print ('Agree:%d.' % agreenum)
                if agreenum==0:
                    print '\n'
                    continue
                p, r = agreenum/matchnum, agreenum/ininum
                f = p*r*2/(p+r)
                print ('Precision: %2f\nRecall: %2f\nF: %2f\n' % (p,r,f))
    print 'agree: ' + str(agree)
    print 'G: ' + str(G)
    print 'N: ' + str(N)
    p, r = agree/N, agree/G
    f = p*r*2/(p+r)
    print ('Precision: %2f\nRecall: %2f\nF: %2f\n' % (p,r,f))
    print 'finished!'


if __name__ == '__main__': main()