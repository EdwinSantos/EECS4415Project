import csv
import re
import sys
import os
import json
import pandas as pd

df = pd.read_csv('tweets.csv')

# home = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#JuveUCL']
# neutral = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#JuveAtleti']
# away = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#A\\u00fapaAtleti']

# export_csv1 = home.to_csv(r'C:\Users\Paul\Desktop\home.csv')
# export_csv2 = neutral.to_csv(r'C:\Users\Paul\Desktop\neutral.csv')
# export_csv3 = away.to_csv(r'C:\Users\Paul\Desktop\away.csv')


home = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#HalaMadrid']
neutral = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#ICICESTPARIS']
away = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#RMAPSG']

export_csv1 = home.to_csv(r'C:\Users\Paul\Desktop\home.csv')
export_csv2 = neutral.to_csv(r'C:\Users\Paul\Desktop\neutral.csv')
export_csv3 = away.to_csv(r'C:\Users\Paul\Desktop\away.csv')