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
data2 = pd.read_csv(sys.argv[2], parse_dates=['timestamp'])
data3 = pd.read_csv(sys.argv[3], parse_dates=['timestamp'])

COLS = ['date', 'text', 'sentiment', 'subjectivity', 'polarity']
df = pd.DataFrame(columns=COLS)
df2 = pd.DataFrame(columns=COLS)
df3 = pd.DataFrame(columns=COLS)

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

for index, row in islice(data2.iterrows(), 0, None):
    new_entry2 = []
    Lower2 = ((row['text']).lower())
    blob2 = TextBlob(Lower)
    sentiment2 = blob.sentiment
    polarity2 = sentiment.polarity
    subjectivity2 = sentiment.subjectivity

    new_entry2 += [row['timestamp'], Lower, sentiment, subjectivity, polarity2]

    single_survey_sentiment_df2 = pd.DataFrame([new_entry2], columns=COLS)
    df2 = df2.append(single_survey_sentiment_df, ignore_index=True)

for index, row in islice(data3.iterrows(), 0, None):
    new_entry3 = []
    Lower = ((row['text']).lower())
    blob3 = TextBlob(Lower)
    sentiment3 = blob.sentiment
    polarity3 = sentiment.polarity
    subjectivity = sentiment.subjectivity

    new_entry3 += [row['timestamp'], Lower, sentiment, subjectivity, polarity3]

    single_survey_sentiment_df3 = pd.DataFrame([new_entry3], columns=COLS)
    df3 = df3.append(single_survey_sentiment_df, ignore_index=True)

## calculate the mean of polarity across all the tweets
sent_df = df['polarity'].mean()
file_name = os.path.basename(sys.argv[1])
file_name2 = os.path.basename(sys.argv[2])
file_name3 = os.path.basename(sys.argv[3])
## print hashtag which used for later + polarity value (negative or positive or neutral statement)
print("Hashtag information and its sentiment value is: " + file_name + " " + str(sent_df), "  ")
print("Hashtag information and its sentiment value is: " + file_name2 + " " + str(sent_df), "  ")
print("Hashtag information and its sentiment value is: " + file_name3 + " " + str(sent_df), "  ")



##df.to_csv('Sentiment_Values.csv', mode='w', columns=COLS, index=False, encoding="utf-8")

## might use later
##hash_tag_retrieval = data.iloc[:, -1]
##hash_tag_retrieval = hash_tag_retrieval.to_string()
##group = re.findall(r"#(\w+)", hash_tag_retrieval)

##dictHashTags = dict.fromkeys(group, )
