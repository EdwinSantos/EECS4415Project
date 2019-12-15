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
    print("Started to build graph")
    matches = json.loads(sys.argv[1])
    global neutraltag
    # Go over all the matches that are passed
    for match in matches:
        neutraltag = match[2]
        fixtureID = match[4]
        # Get the events that were queried after the match ended
        match_events = get_match_events(fixtureID)
        # Get the sentiments that were calculated previously
        twitter_sentiment = get_sentiment(fixtureID)
        build_graph(match_events, twitter_sentiment, match)


def build_graph(match_events, twitter_sentiment, match):
    start_time, end_time, events = handle_events(match_events)
    # Set the parameters for the graph
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.set_xlim([start_time, end_time])
    ax.set_ylim([-10, 10])
    # Plot all the events with their respective text on the graph
    for event in events:
        plt.axvline(event[0])
        plt.text(event[0], -9, event[1], rotation=90)

    times = twitter_sentiment["EndOfTimeWindow"].values
    fixturetimes = []
    for time in times:
        fixturetimes.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
    home = twitter_sentiment["Home Team"].values
    away = twitter_sentiment["Away team"].values
    neutral = twitter_sentiment["Neutral"].values
    plt.plot(fixturetimes, home, '.r-', label=match[0])
    plt.plot(fixturetimes, away, '.b-', label=match[1])
    plt.plot(fixturetimes, neutral, '.g-', label=match[2])
    plt.legend(loc="upper left")
    plt.xlabel("Time")
    plt.ylabel("Sentiment")
    plt.show()
    plt.savefig(os.path.join("#" + match[2], match[2] + ".png"))


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
        # Get rid of subs because it creates too many events
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
    match_events = json.dumps(json_response)
    return match_events


def get_sentiment(fixtureID):
    data = pd.read_csv(os.path.join("#" + neutraltag, str(fixtureID) + ".csv"))
    return data


if __name__ == "__main__": main()
