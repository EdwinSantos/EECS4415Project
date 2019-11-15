#!/usr/bin/python

import csv
import re
import sys

with open('tweets.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(('timestamp', 'text', 'hashtags'))
    lines = sys.stdin
    for line in lines:
        line = line.strip()
        line = re.sub(r'^"', '', line)
        line = re.sub(r'"$', '', line)
        line = re.split(r'\\t', line)
        writer.writerow(line)
