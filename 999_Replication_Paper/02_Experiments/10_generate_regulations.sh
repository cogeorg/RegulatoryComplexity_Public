#!/bin/bash
OUT_DIR=./10_regulations/
NODE_LIST=10_node_list_wgt.txt

# rm $OUT_DIR/* 2>/dev/null

for ((i=1; i<=8000; i++))
do
    python 10_random_regulation_generator3.py $NODE_LIST $OUT_DIR
done

cd 10_regulations
for i in `ls *.tex` ; do pdflatex $i; done
rm *.aux *.log 2>/dev/null
cd ..
