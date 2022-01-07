#!/bin/bash
BASE_DIR=~/Downloads/Data/

cd 30_results ; rm *.csv ; cd ..
for file_name in $BASE_DIR/20_complexities/*.csv ;
   do python 30_analyze_complexity.py $file_name $BASE_DIR/30_results/ ;
done

cd $BASE_DIR/30_results
    for j in `seq 0 9` ;
        do for i in `ls *-$j*.csv` ;
            do cat $i >> results_all.csv ;
        done ;
    done
cd -
