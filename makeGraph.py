#!/usr/bin/python

import json
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests

debugging = False


def main():
    match_events = get_match_events(240579)
    twitter_sentiment = get_sentiment()
    print(twitter_sentiment)
    build_graph(match_events, twitter_sentiment)

def get_sentiment():
    data = pd.read_csv("Results.csv")
    return data


def build_graph(match_events, twitter_sentiment):
    start_time, end_time, events = handle_events(match_events)

    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.set_xlim([start_time, end_time])
    ax.set_ylim([-8, 3])
    for event in events:
        plt.axvline(event[0])
        print(event[1])
        plt.text(event[0], -8, event[1], rotation=90)

    times = twitter_sentiment["EndOfTimeWindow"].values
    fixtimes = []
    for time in times:
        fixtimes.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
    home = twitter_sentiment["Home Team"].values
    away = twitter_sentiment["Away team"].values
    neutral = twitter_sentiment["Neutral"].values
    print(times)
    plt.plot(fixtimes, home, '.r-', label="#HalaMadrid")
    plt.plot(fixtimes, away, '.b-', label="#ICICESTPARIS")
    plt.plot(fixtimes, neutral, '.g-',label="#RMAPSG")
    plt.legend(loc="upper left")

    plt.xlabel("Time")
    plt.ylabel("Sentiment")
    plt.show()

    # Add events here


def handle_events(match_events):
    all_events = []
    json_events = json.loads(match_events)
    event_df = pd.DataFrame()

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
        detail = str(game_time) + " " + event["detail"] + " " + event["player"] + " (" + event["teamName"] + ")"

        if game_time >= 45:
            game_time = game_time + 15
        timestamp = datetime.fromtimestamp(graph_start_time_unix + 900 + (game_time * 60))
        moment = [timestamp, detail]
        all_events.append(moment)

    return graph_start_time, graph_end_time, all_events


def get_fixtureID(home_team_id, away_team_id):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/" + str(home_team_id) + "/" + str(league_id)

    # Real code
    # response = query_api(url)
    # json_response = json.load(response)

    # Debug code
    with open("fixtureID.json", encoding="utf8") as json_file:
        json_response = json.load(json_file)

    for fixture in json_response["api"]["fixtures"]:
        targetFixture_id = 0
        if (fixture["homeTeam"]["team_id"] == home_team_id and fixture["awayTeam"]["team_id"] == away_team_id and
                fixture["league_id"] == 524 and fixture["status"] == "Match Finished"):
            targetFixture_id = fixture["fixture_id"]
            break
        # Error catching stuff should go here.
    return targetFixture_id


def get_match_events(fixture_ID):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/id/" + str(fixture_ID)
    #response = query_api(url)
    #json_response = json.loads(response)
    #with open('data.json', 'w') as f:
    #    json.dump(response, f)

    with open('data.json', 'r') as myfile:
        data = myfile.read()
    json_response = json.loads(data)
    print(type(json_response))
    match_events = json.dumps(json_response["api"]["fixtures"][0])
    return match_events


def query_api(url):
    querystring = {"timezone": "Europe/London"}

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': get_key()
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text


def get_key():
    file = open("key.txt", "r")
    return file.read()

if __name__ == "__main__": main()
