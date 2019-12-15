#!/usr/bin/python

import json
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
import json

debugging = False

neutraltag = ""

def main():
    matches = json.loads(sys.argv[1])
    # Go over all the matches that are passed
    global neutraltag
    for match in matches:
        hometag = match[0]
        awaytag = match[1]
        neutraltag = match[2]
        timestamp = match[3]
        fixtureID = match[4]
        match_events = get_match_events(fixtureID)
        # Pass whatever detail you need to get the results file
        twitter_sentiment = get_sentiment(fixtureID)
        print(twitter_sentiment)
        build_graph(match_events, twitter_sentiment, match)


def get_sentiment(fixtureID):
    data = pd.read_csv(os.path.join("#" + neutraltag, str(fixtureID) + ".csv"))
    return data


def build_graph(match_events, twitter_sentiment, match):
    start_time, end_time, events = handle_events(match_events)

    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.set_xlim([start_time, end_time])
    ax.set_ylim([-10, 10])
    for event in events:
        plt.axvline(event[0])
        print(event[1])
        plt.text(event[0], -9, event[1], rotation=90)

    times = twitter_sentiment["EndOfTimeWindow"].values
    fixtimes = []
    for time in times:
        fixtimes.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
    home = twitter_sentiment["Home Team"].values
    away = twitter_sentiment["Away team"].values
    neutral = twitter_sentiment["Neutral"].values
    print(times)
    plt.plot(fixtimes, home, '.r-', label=match[0])
    plt.plot(fixtimes, away, '.b-', label=match[1])
    plt.plot(fixtimes, neutral, '.g-', label=match[2])
    plt.legend(loc="upper left")

    plt.xlabel("Time")
    plt.ylabel("Sentiment")
    plt.show()


def handle_events(match_events):
    all_events = []
    json_events = json.loads(match_events)

    # Create extra events that aren't provided
    # Start time = start_time - extra coverage
    graph_start_time_unix = json_events["firstHalfStart"] - 900
    graph_start_time = datetime.fromtimestamp(graph_start_time_unix)

    # Endtime = start_time + match lenght + extra coverage
    graph_end_time_unix = json_events["firstHalfStart"] + 6300 + 900
    graph_end_time = datetime.fromtimestamp(graph_end_time_unix)

    first_half_start = datetime.fromtimestamp(graph_start_time_unix + 900)
    all_events.append([first_half_start, "Match Start"])

    first_half_end = datetime.fromtimestamp(graph_start_time_unix + 900 + 2700)
    all_events.append([first_half_end, "First Half Ends"])
    second_half_start = datetime.fromtimestamp(graph_end_time_unix - 900 - 2700)
    all_events.append([second_half_start, "Second Half Starts"])
    second_half_end = datetime.fromtimestamp(graph_end_time_unix - 900)
    all_events.append([second_half_end, "Match Ends"])

    for event in json_events["events"]:
        game_time = event["elapsed"]
        # Get rid of subsitutions because it creates too many events
        if event["type"] == "subst":
            continue
        detail = str(game_time) + " " + event["detail"] + " " + event["player"] + " (" + event["teamName"] + ")"

        if game_time >= 45:
            game_time = game_time + 15
        timestamp = datetime.fromtimestamp(graph_start_time_unix + 900 + (game_time * 60))
        moment = [timestamp, detail]
        all_events.append(moment)

    return graph_start_time, graph_end_time, all_events


def get_match_events(fixture_ID):
    with open(str(fixture_ID) + '.json', 'r') as match_events_file:
        match_events = match_events_file.read()
    json_response = json.loads(match_events)
   #match_events = json.dumps(json_response["api"]["fixtures"][0])

    match_events = json.dumps(json_response)
    return match_events


if __name__ == "__main__": main()
