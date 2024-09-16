#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# OPTIMIZED FOR OS X

__author__="""Co-Pierre Georg (c.georg@fs.de)"""

import pandas as pd
import random
import json
import requests
import os
import re
import ast
import sys
import nltk
import string

from collections import Counter
from tqdm import trange, tqdm
tqdm.pandas()

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import bigrams, trigrams, ngrams

from myfunctions import *


# ###########################################################################
#
# METHODS
#
# ###########################################################################

def remove_ngrams_raw(in_file_name, ngram_file_name, out_file_name):
    # Step 2: Read the contents of the input file
    with open(in_file_name, 'r') as file:
        in_text = file.read()

    # Step 3: Read the strings to be removed from bla.csv (assuming a single column)
    df_out = pd.read_csv(ngram_file_name, header=None)
    strings_to_remove = df_out[0].tolist()

    print("Before removing: ", len(in_text))

    # Step 4: Initialize a dictionary to store the count of occurrences for each string
    occurrences = {}

    # Step 5: Loop through each string in bla.csv and remove it from in_text (case insensitive)
    for string_ in strings_to_remove:
        # Count occurrences of the string (case insensitive)
        count = len(re.findall(re.escape(string_), in_text, flags=re.IGNORECASE))
        
        # Save the count of occurrences
        occurrences[string_] = count
        
        # Remove all occurrences (case insensitive)
        in_text = re.sub(re.escape(string_), '', in_text, flags=re.IGNORECASE)

    # Step 6: Print the number of occurrences for each string
    for string_, count in occurrences.items():
        print(f"n-gram '{string_}' found {count} times and removed.")

    # Step 7: Save the modified text
    with open(out_file_name, 'w') as file:
        file.write(in_text)

    print("After removing: ", len(in_text))
    print(f"Text processing complete. Cleaned text saved to {out_file_name}")


def do_run(action, args):
    if action == "1":
        # convention for args is: in_file_name, ngram_file_name, out_file_name
        remove_ngrams_raw(args[0], args[1], args[2])

# ###########################################################################
#
#  MAIN
#
# ###########################################################################
if __name__ == '__main__':
#
# VARIABLES
#
    args = sys.argv
    action = args[1]

#
# CODE
#
    do_run(action, args[2:])
