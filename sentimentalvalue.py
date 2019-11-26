import re
import pandas as pd
import os
import sys
from textblob import TextBlob
from itertools import islice
from os import listdir

## used for reading multiple csv files in directory
CSV_Files = [file for file in listdir(os.getcwd()) if file.endswith('.csv')]
dataframe_list = [pd.read_csv(csv_name) for csv_name in CSV_Files]
print(dataframe_list)
## dictionary to hold hashtags and their sentimental value
dictHashTags = []
## parse the dates of tweets
## data = pd.read_csv("tweets.csv", parse_dates=['timestamp'])
##data = pd.read_csv(sys.argv[1], parse_dates=['timestamp'])
##data2 = pd.read_csv(sys.argv[2], parse_dates=['timestamp'])
##data3 = pd.read_csv(sys.argv[3], parse_dates=['timestamp'])

COLS = ['date', 'text', 'sentiment', 'subjectivity', 'polarity']
df = pd.DataFrame(columns=COLS)
df2 = pd.DataFrame(columns=COLS)
df3 = pd.DataFrame(columns=COLS)


## apply sent value on tweets
for index, row in islice(dataframe_list[0].iterrows(), 0, None):
    new_entry = []
    Lower = ((row['text']).lower())
    blob = TextBlob(Lower)
    sentiments = blob.sentiment
    polarity = sentiments.polarity
    subjectivity = sentiments.subjectivity

    new_entry += [row['timestamp'], Lower, sentiments, subjectivity, polarity]
    single_survey_sentiment_df = pd.DataFrame([new_entry], columns=COLS)
    df = df.append(single_survey_sentiment_df, ignore_index=True)

for index, row in islice(dataframe_list[1].iterrows(), 0, None):
    new_entry2 = []
    Lower2 = ((row['text']).lower())
    blob2 = TextBlob(Lower2)
    sentiment2 = blob2.sentiment
    polarity2 = sentiment2.polarity
    subjectivity2 = sentiment2.subjectivity

    new_entry2 += [row['timestamp'], Lower2, sentiment2, subjectivity, polarity2]

    single_survey_sentiment_df2 = pd.DataFrame([new_entry2], columns=COLS)
    df2 = df2.append(single_survey_sentiment_df2, ignore_index=True)
for index, row in islice(dataframe_list[2].iterrows(), 0, None):
    new_entry3 = []
    Lower3 = ((row['text']).lower())
    blob3 = TextBlob(Lower3)
    sentiment3 = blob3.sentiment
    polarity3 = sentiment3.polarity
    subjectivity3 = sentiment3.subjectivity

    new_entry3 += [row['timestamp'], Lower3, sentiment3, subjectivity, polarity3]

    single_survey_sentiment_df3 = pd.DataFrame([new_entry3], columns=COLS)
    df3 = df3.append(single_survey_sentiment_df3, ignore_index=True)

COL = ['EndOfTimeWindow', 'Home Team Sentiment', 'Away team', 'Neutral']
final_df = pd.DataFrame(columns=COL)

sent_df = df['polarity'].mean()
sent_df2 = df2['polarity'].mean()
sent_df3 = df3['polarity'].mean()

new_entry4 = []
new_entry4 += ['timestamp'+str(+ 300), sent_df, sent_df2, sent_df3]

final = pd.DataFrame([new_entry4], columns=COL)
final_df = final_df.append(final, ignore_index=True)
print(df)
final_df.to_csv(r'C:\Users\AmirYounesi\PycharmProjects\bigdata\b\SentimentValues.csv', mode='w', columns=COL, index=False, encoding="utf-8")



## calculate the mean of polarity across all the tweets






## might use later
##hash_tag_retrieval = data.iloc[:, -1]
##hash_tag_retrieval = hash_tag_retrieval.to_string()
##group = re.findall(r"#(\w+)", hash_tag_retrieval)

##dictHashTags = dict.fromkeys(group, )
