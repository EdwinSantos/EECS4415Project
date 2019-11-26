#!/usr/bin/python

import csv
import re
import sys
import os

# dir = './dump'
# Directory of txt dump files
os.chdir('./dump')

with open('tweets.csv', 'a+', newline ='') as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(('timestamp', 'text', 'hashtags'))

    for filename in os.listdir('.'):
        with open(filename, 'r', encoding='utf-16') as txtfile:
            lines = txtfile.readlines()

            for line in lines:
                line = line.strip()
                line = re.sub(r'^"', '', line)
                line = re.sub(r'"$', '', line)
                line = re.split(r'\\t', line)
                writer.writerow(line)



# with open('tweets.csv', 'r+', newline ='') as readcsv:
#     spamreader = csv.DictReader(readcsv)
#     # sortedlist = sorted(spamreader, key=lambda row: row[2], reverse=False )
#     print(spamreader)


# with open('sortedtweets.csv', 'w+') as sortedfile:
#     fieldnames = ['timestamp', 'text', 'hashtags']
#     # writer = csv.DictWriter(sortedfile, lineterminator = '\n')
#     # writer.writerow(('timestamp', 'text', 'hashtags'))
#     sortwriter = csv.DictWriter(sortedfile, fieldnames=fieldnames)
#     sortwriter.writeheader()
#     for row in sortedlist:
#         writer.writerow(row)
