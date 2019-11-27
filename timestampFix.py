#!/usr/bin/python

import csv
import re
import sys
import os
import json

# dir = './dump'
# Directory of txt dump files
tag = sys.argv[1]
os.chdir('./csv')
first = True
original = tag + ".csv"
fixed = tag + " - Fixed.csv"
with open(original, 'r') as f:
    reader = csv.reader(f,delimiter=",")
    with open(fixed, 'a+', newline='') as csvf:
        writer = csv.writer(csvf, lineterminator = '\n')
        writer.writerow(('timestamp', 'text', 'hashtags'))
        for row in reader:
            if first:
                first = False
                continue
            row[0] = str(int(row[0]) - 18000)
            writer.writerow(row)