import csv
import re
import sys
import os
import json
import pandas as pd

df = pd.read_csv('tweets.csv')

asdf = df[['timestamp','text','hashtags']].loc[df['hashtags'] == '#JuveAtleti']
export_csv = asdf.to_csv(r'C:\Users\Paul\Desktop\export_dataframe.csv')
