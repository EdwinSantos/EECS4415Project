import re
import pandas as pd
from textblob import TextBlob
from itertools import islice

## dictionary to hold hashtags and their sentimental value
dictHashTags = []
## parse the dates of tweets
data = pd.read_csv("tweets.csv", parse_dates=['timestamp'])
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

##
df.to_csv('Sentiment_Values.csv', mode='w', columns=COLS, index=False, encoding="utf-8")
print(df[df.date.dt.strftime('%H:%M:%S').between('06:00', '06:30')])
##df['date'] = df[df.set_index('date') < '06:30:00'].reset_index()

##print(df)

## needed for later 
##hash_tag_retrieval = data.iloc[:, -1]
##hash_tag_retrieval = hash_tag_retrieval.to_string()
##group = re.findall(r"#(\w+)", hash_tag_retrieval)

##dictHashTags = dict.fromkeys(group, )

##new_df = data.set_index(['timestamp']).sort_index()

##
##data = data.reset_index().set_index('timestamp')
##new_df = data.resample("T")

