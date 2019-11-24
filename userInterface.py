#!/usr/bin/python

import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests

league_id = 524

teams = {
    "Liverpool": 40,
    "Norwich": 71,
    "West_Ham": 48,
    "Manchester_City": 50,
    "Bournemouth": 35,
    "Sheffield_Utd": 62,
    "Burnley": 44,
    "Southampton": 41,
    "Crystal_Palace": 52,
    "Everton": 45,
    "Leicester": 46,
    "Wolves": 39,
    "Watford": 38,
    "Brighton": 51,
    "Tottenham": 47,
    "Aston_Villa": 66,
    "Newcastle": 34,
    "Arsenal": 42,
    "Manchester United": 33,
    "Chelsea": 49,
}

debugging = False


def main():
    global debugging
    debugging = (input("Running in debug mode (Y/N): ") == "Y")
    print(debugging)
    # Replace this with a list of teams taken from the API
    if not debugging:
        for team in teams:
            print(repr(team), ":", teams[team])
        home_team_id = int(input("Enter home team number: "))
        way_team_id = int(input("Enter away team number: "))
        home_team_hashtag = input("Enter home team hashtag: ")
        away_team_hashtag = input("Enter away team hashtag: ")
        neutral_team_hashtag = input("Enter neutral hashtag: ")
    else:
        home_team_id = 49
        away_team_id = 52
        home_team_hashtag = "#Chelsea"
        away_team_hashtag = "#Crystal_Palace"
        neutral_team_hashtag = "#CheVSCry"

    # pass hashtags to twitter class that will take care of getting the tweets
    fixture_ID, timestamp = get_fixtureID(home_team_id, away_team_id)
    match_events = get_match_events(fixture_ID)
    # pass events and tweet ratings to class that will make the graph
    build_graph(match_events)


def build_graph(match_events):
    start_time, end_time, events = handle_events(match_events)

    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.set_xlim([start_time, end_time])
    for event in events:
        plt.axvline(event[0])
        print(event[1])
        plt.text(event[0], 0, event[1], rotation=90)
    plt.xlabel("Time")
    plt.ylabel("Sentiment")
    plt.show()
    plt.savefig("Graph")

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
            timestamp = fixture["event_date"]
            break
        # Error catching stuff should go here.
    return targetFixture_id, timestamp


def get_match_events(fixture_ID):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/id/" + str(fixture_ID)
    print(debugging)
    if debugging:
        with open("MatchEvents.json", encoding="utf8") as json_file:
            json_response = json.load(json_file)
    else:
        response = query_api(url)
        json_response = json.load(response.read())

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
