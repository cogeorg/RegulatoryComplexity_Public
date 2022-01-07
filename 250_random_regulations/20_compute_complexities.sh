#!/bin/bash
BASE_DIR=.

# python3 20_compute_complexity.py tmp.txt 20_complexities/ ;
python3 20_compute_complexity.py baseli_algorithm.txt 20_complexities/ ;

# for file_name in $BASE_DIR/10_regulations/*.txt ;
#     do python3 20_compute_complexity.py $file_name ~/Downloads/Data/20_complexities/ ;
# done
