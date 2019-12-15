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

# Iterate through each match folder, reading all files and organizing them by hashtags
for match in ht:
    os.chdir(match[2])

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

    # Read csv as dataframes split between the hashtags, and create a separate csv 
    # for each hashtag
    df = pd.read_csv('tweets.csv')
    home = df[['timestamp','text','hashtags']].loc[df['hashtags'] == match[0]]
    neutral = df[['timestamp','text','hashtags']].loc[df['hashtags'] == match[2]]
    away = df[['timestamp','text','hashtags']].loc[df['hashtags'] == match[1]]

    export_csv1 = home.to_csv(match[0] + '.csv', index=False)
    export_csv2 = neutral.to_csv(match[2] + '.csv', index=False)
    export_csv3 = away.to_csv(match[1] + '.csv', index=False)

    os.chdir('..')