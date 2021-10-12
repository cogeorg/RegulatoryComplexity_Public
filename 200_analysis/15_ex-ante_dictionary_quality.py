#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re

# ###########################################################################
# METHODS
# ###########################################################################

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(master_dict_file, title_dict_file, results_file):
    out_text = ""
    master_dict = {}
    dict_current = {}

    print("<<< 15_EX-ANTE_DICTIONARY_QUALITY.PY")

    #
    # LOAD DICTIONARIES
    #
    dict_file = open(master_dict_file, "r")
    dict_file.readline()
    for line in dict_file.readlines():
        tokens = line.strip().split("\t")
        try:
            master_dict[tokens[0].strip('"')] = tokens[2].strip('"')
        except:
            pass
    dict_file.close()

    dict_file = open(title_dict_file, "r")
    for line in dict_file.readlines():
        tokens = line.strip().split(";")
        try:
            dict_current[tokens[0].strip('"')] = tokens[2].strip('"')
        except:
            pass
    dict_file.close()

    print("  <<< READ MASTER DICT: " + master_dict_file + " WITH " + str(len(master_dict)) + " ENTRIES")
    print("  <<< READ CURRENT DICT: " + title_dict_file + " WITH " + str(len(dict_current)) + " ENTRIES")

    # for each entry in current dict, check how often it occurs in master dict
    for key_current in dict_current.keys():
        if key_current in master_dict.keys():
            excess_count = int(master_dict[key_current]) - int(dict_current[key_current])
            out_text += key_current + ";" + str(excess_count) + "\n"
        else:
            pass  # only happens in title 0 for some weird reason and only for ~10 entries fix later
            # print("NO SUCH LUCK: ", key_current)

    out_file = open(results_file, "w")
    out_file.write(out_text)
    out_file.close()
    print("  <<< WRITTEN RESULTS TO: " + results_file)

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
    master_dict_file = args[1]
    title_dict_file = args[2]
    results_file = args[3]

#
# CODE
#
    do_run(master_dict_file, title_dict_file, results_file)
