import datetime
import glob
import sys
from os.path import isfile, join
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd
import os
import pandas as pd
import nltk
from datetime import datetime

nltk.download('vader_lexicon')
COL = ['EndOfTimeWindow', 'Home Team', 'Away team', 'Neutral']

starttime = 1574798400
endtime = (1574798400 + 7200)
sia = SIA()


def main():
    hashtagtypes = ["Home", "Away", "Neutral"]
    # Read files one at a time into dataframes
    home_df = pd.read_csv(os.path.join("csv", "Home-HalaMadrid.csv"))
    away_df = pd.read_csv(os.path.join("csv", "Away-ICICESTPARIS.csv"))
    neutral_df = pd.read_csv(os.path.join("csv", "Neutral-RMAPSG.csv"))
    home_results = process_dfs(home_df)
    away_results = process_dfs(away_df)
    neutral_results = process_dfs(neutral_df)
    home_df = pd.DataFrame(home_results)
    away_df = pd.DataFrame(away_results)
    neutral_df = pd.DataFrame(neutral_results)
    test = pd.merge(home_df, away_df, on=0)
    output_df = pd.merge(test, neutral_df, on=0)
    output_df.columns = COL
    output_df.to_csv("Results.csv", index=False)

    print(output_df)


# Process dataframe to get sentiment value
def process_dfs(home_df):
    total_average = 0
    score = 0
    count = 0
    result = []
    time = []
    for i in range(starttime, endtime, 300):
        first_timeslot = home_df.loc[(home_df['timestamp'] >= i) & (home_df['timestamp'] <= (i + 300))]
        for row in first_timeslot.iterrows():
            score = score + sia.polarity_scores(row[1][1]).get("compound")
            count = count + 1
        if count == 0:
            total_average = 0
        else:
            total_average = score / count
        result.append([datetime.fromtimestamp(i + 300), total_average*10])
    return result

    # Add value to column in dataframe

    # Output the output dataframe


if __name__ == "__main__": main()
