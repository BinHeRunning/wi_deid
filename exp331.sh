#!/bin/sh
# ./Auto.sh ./ > out
# $1 is the exp folder

echo "exp324jd, jia data dic, qu dian, new patterns,template_try4_3"
# Step1-PrepareTrainingdata
#python Preprocessing1.py ./data train
#javac -Djava.ext.dirs=./lib ST.java
#java -Djava.ext.dirs=./lib ST ./data ./models train
#python Preprocessing2_new2.py ./data train
#cd geniatagger-3.0.1
#./geniatagger < ../data/tempdata/train.tok > ../data/tempdata/train.tpc
#cd ..
#python AddfeatureAndCombine1.py ./data train "$1"

# Step2-PrepareTestdata
#python Preprocessing1.py ./data test
#javac -Djava.ext.dirs=./lib ST.java
#java -Djava.ext.dirs=./lib ST ./data ./models test
#python Preprocessing2_new2.py ./data test
#cd geniatagger-3.0.1
#./geniatagger < ../data/tempdata/test.tok > ../data/tempdata/test.tpc
#cd ..
#python AddfeatureAndCombine1.py ./data test "$1"

#python AddDicFeatures.py ./traindic train.data train324jd.data test.data test324jd.data

crf_learn -f 4 -c 101 -p 20 template_try4_3 train324jd.data model331jd

crf_test -m model331jd test324jd.data > testresult331jd.out

python TransTestresult.py ./ ./data testresult331jd.out testing_result331jd test324jd.data

python Evaluate.py ./data ./ testing_result331jd
