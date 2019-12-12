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

starttime = 0
endtime = 0
sia = SIA(


def main():
    hashtagtypes = ["Home", "Away", "Neutral"]
    match_info = get_info_from_files()
    for match in matches:
        build_graph(match)


def build_graph(match):
    # Read files one at a time into dataframes
    # home_df = pd.read_csv(os.path.join("csv", "Home-JuveUCL.csv"))
    home_df = match.hometag
    #away_df = pd.read_csv(os.path.join("csv", "Away-AupaAtleti.csv"))
    away_df = match.awaytag
    neutral_df = match.neurtraltag
    #neutral_df = pd.read_csv(os.path.join("csv", "Neutral-JuveAtleti.csv"))

    starttime = match.starttime
    endtime = match.endtime 
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


def get_info_from_files():
    #Go to [fileName] to get the name of the folder that im looking for + names of the files that im looking for
    #From that get the timestamp, hashtag and sentiment values and process them
    return x

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
