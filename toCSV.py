#!/usr/bin/python

import csv
import re
import sys
import os
import json
import pandas as pd
from contextlib import suppress

matches = json.loads(sys.argv[1])
ht = []
# make list of hashtags (i.e., remove timestamp + other unwanted information) format: [[home, away, neutral], [...]]
for game in matches:
    ls = []
    if "#" not in game[0]:
        ls.append("#" + game[0])
    else:
        ls.append(game[0])
    if "#" not in game[1]:
        ls.append("#" + game[1])
    else:
        ls.append(game[1])
    if "#" not in game[2]:
        ls.append("#" + game[2])
    else:
        ls.append(game[2])
    ht.append(ls)

# matchlist =   [["SUFC", "AVFC", "SUFAVL"], ["LCFC", "NCFC", "LeiNor"]]

# Iterate through each match folder, reading all files and organizing them by hashtags
for match in ht:
    os.chdir('#' + match[2])

    with suppress(Exception):
        with open('tweets.csv', 'a+', newline ='') as csvfile:
            writer = csv.writer(csvfile, lineterminator = '\n')
            writer.writerow(('timestamp', 'text', 'hashtags'))

            for filename in os.listdir('.'):
                with open(filename, 'r', encoding='utf-16' ) as txtfile:
                    lines = txtfile.readlines()

                    for line in lines:
                        line = line.strip()
                        line = re.sub(r'^"', '', line)
                        line = re.sub(r'"$', '', line)
                        line = re.split(r'\\t', line)
                        writer.writerow(line)

    df = pd.read_csv('tweets.csv')
    home = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#' + match[0]]
    neutral = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#' + match[2]]
    away = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#' + match[1]]

    # export_csv1 = home.to_csv('home.csv', index=False)
    # export_csv2 = neutral.to_csv('neutral.csv', index=False)
    # export_csv3 = away.to_csv('away.csv', index=False)

    export_csv1 = home.to_csv('#' + match[0] + '.csv', index=False)
    export_csv2 = neutral.to_csv('#' + match[2] + '.csv', index=False)
    export_csv3 = away.to_csv('#' + match[1] + '.csv', index=False)

    os.chdir('..')





    # export_csv1 = home.to_csv(r'C:\Users\Paul\Desktop\home.csv', index=False)
    # export_csv2 = neutral.to_csv(r'C:\Users\Paul\Desktop\neutral.csv', index=False)
    # export_csv3 = away.to_csv(r'C:\Users\Paul\Desktop\away.csv', index=False)

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


# # format: [[Hometag, Awaytag, Neutraltag, Timestamp, ...], [...]]
# print(sys.argv[1])
# matches = json.loads(sys.argv[1])
# tracking = []
# ht = []
# neutral_tags = []
# # make list of hashtags (i.e., remove timestamp + other unwanted information) format: [[home, away, neutral], [...]]
# for game in matches:
#     ls = []
#     if "#" not in game[0]:
#         ls.append("#" + game[0])
#     else:
#         ls.append(game[0])
#     if "#" not in game[1]:
#         ls.append("#" + game[1])
#     else:
#         ls.append(game[1])
#     if "#" not in game[2]:
#         ls.append("#" + game[2])
#     else:
#         ls.append(game[2])
#     ht.append(ls)