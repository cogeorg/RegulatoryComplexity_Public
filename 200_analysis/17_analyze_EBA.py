#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# OPTIMIZED FOR OS X

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re

# ###########################################################################
# METHODS
# ###########################################################################

# ENSURE THAT THIS METHOD IS THE SAME AS IN 13_STANDARDIZE_MASTER.PY
def clean(value):
    value = value.replace("\n", "")

    value = value.replace("'", "")
    value = value.replace(".", "")
    value = value.replace(",", "")
    value = value.replace(";", "")
    value = value.replace(":", "")
    value = value.replace('"', '')
    value = value.replace("`", "")
    value = value.replace("$", "")

    value = value.replace("(", "")
    value = value.replace(")", "")

    value = value.replace("``", "")
    value = value.replace("--", "")

    value = value.upper()

    return value


# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_dir, dict_file_name, output_dir):
    dict = {}

    print("<<< 15_ANALYZE_AGENCYLETTERS.PY")

    #
    # LOAD CONSOLIDATED DICTIONARY
    #
    dict_file = open(dict_file_name, "r")
    dict_file.readline()  # ignore header when using Master_v1.0.csv
    for line in dict_file.readlines():
        tokens = line.strip().split(";")
        dict[tokens[0].strip('"')] = tokens[1].strip('"').strip()
    print("  <<< READ DICTIONARY: " + dict_file_name + " WITH " + str(len(dict)) + " ENTRIES")

    # dict.sort(key=len, reverse=True)

    if False:
        for key in sorted(dict, key=len, reverse=True):
            print(key, "-->", dict[key])

    #
    # LOOP OVER ALL FILES IN DIRECTORY AND FIND OCCURRENCE OF EACH DICT ENTRY
    #
    for input_file_name in os.listdir(input_dir):
        in_text = ""
        out_text = ""

        # with open(base_directory + input_file_name, encoding="utf-8", errors='replace') as infile:
        try:
            input_file = open(input_dir + "/" + input_file_name, encoding='utf-8', errors='replace')
            out_file = open(output_dir + "/" + "cons-count_" + input_file_name.rstrip(".txt") + ".csv", 'w')
            residual_file = open(output_dir + "/" + "residual_cons-count_" + input_file_name.rstrip(".txt") + ".txt", 'w')

            print("  <<< NOW WORKING ON: " + input_dir + input_file_name)

            for line in input_file.readlines():
                in_text += clean(line.strip())

            for key in sorted(dict, key=len, reverse=True):
                _count = in_text.count(key)
                if _count > 0:
                    out_text += input_file_name + ";" + key + ";" + dict[key] + ";" + str(_count) + "\n"
                    in_text = in_text.replace(key, "")

            if False:
                print(in_text)

            out_file.write(out_text)
            out_file.close()
            residual_file.write(in_text)
            residual_file.close()
        except IsADirectoryError:
            print("<<< SKIPPED:" + input_dir + "/" + input_file_name)

# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
#
#  MAIN
#
# -------------------------------------------------------------------------
if __name__ == '__main__':
#
# VARIABLES
#
    args = sys.argv
    input_dir = args[1]
    dict_file_name = args[2]
    output_file_name = args[3]

#
# CODE
#
    do_run(input_dir, dict_file_name, output_file_name)
