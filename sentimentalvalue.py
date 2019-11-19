import re
import pandas as pd
import os
import sys
from textblob import TextBlob
from itertools import islice
from os import listdir

## used for reading multiple csv files in directory
##CSV_Files = [file for file in listdir('<path to folder>') if file.endswith('.csv')

## dictionary to hold hashtags and their sentimental value
dictHashTags = []
## parse the dates of tweets
## data = pd.read_csv("tweets.csv", parse_dates=['timestamp'])
data = pd.read_csv(sys.argv[1], parse_dates=['timestamp'])
COLS = ['date', 'text', 'sentiment', 'subjectivity', 'polarity']
df = pd.DataFrame(columns=COLS)



## apply sent value on tweets
for index, row in islice(data.iterrows(), 0, None):
    new_entry = []
    Lower = ((row['text']).lower())
    blob = TextBlob(Lower)
    sentiment = blob.sentiment
    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity

    new_entry += [row['timestamp'], Lower, sentiment, subjectivity, polarity]

    single_survey_sentiment_df = pd.DataFrame([new_entry], columns=COLS)
    df = df.append(single_survey_sentiment_df, ignore_index=True)

## calculate the mean of polarity across all the tweets
sent_df = df['polarity'].mean()
file_name =  os.path.basename(sys.argv[1])
## print hashtag which used for later + polarity value (negative or positive or neutral statement)
print("Hashtag information and its sentiment value is: " + file_name + " " + str(sent_df), "  ")

df.to_csv('Sentiment_Values.csv', mode='w', columns=COLS, index=False, encoding="utf-8")

## might use later
##hash_tag_retrieval = data.iloc[:, -1]
##hash_tag_retrieval = hash_tag_retrieval.to_string()
##group = re.findall(r"#(\w+)", hash_tag_retrieval)

##dictHashTags = dict.fromkeys(group, )
