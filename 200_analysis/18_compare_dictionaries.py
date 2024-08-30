#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# OPTIMIZED FOR OS X

import csv
import sys

def read_keys_from_csv(file_name):
    """Reads the keys from the first column of a semicolon-separated CSV file and returns them as a set with all keys capitalized."""
    keys = set()
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=';')  # Specify semicolon as the delimiter
        for row in reader:
            key = row[0].strip().upper()  # Capitalize the key from the first column
            keys.add(key)
    return keys

def write_residuals_to_csv(input_file, output_file, keys_to_include):
    """Writes the entries from input_file where the key is in keys_to_include to output_file."""
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')
        for row in reader:
            key = row[0].strip().upper()
            if key in keys_to_include:
                writer.writerow(row)

def compare_and_write_residuals(file1, file2):
    """Compares the keys in the first column of two semicolon-separated CSV files and writes out residuals."""
    keys1 = read_keys_from_csv(file1)
    keys2 = read_keys_from_csv(file2)

    unique_to_file1 = keys1.difference(keys2)
    unique_to_file2 = keys2.difference(keys1)

    print(f"Number of keys in {file1} but not in {file2}: {len(unique_to_file1)}")
    print(f"Number of keys in {file2} but not in {file1}: {len(unique_to_file2)}")

    write_residuals_to_csv(file1, str(file1) + '_residual.csv', unique_to_file1)
    write_residuals_to_csv(file2, str(file2) + '_residual.csv', unique_to_file2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_keys.py <file1.csv> <file2.csv>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    compare_and_write_residuals(file1, file2)