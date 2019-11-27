#!/usr/bin/python

import json
import os

import requests

league_id = 524

leagues = {
    "Champions League": 530,
    "Premier League": 524,
    "Championship": 565
}

modes = {
    "Tweet Farming": 1,
    "Tweet Analyzing": 2,
    "Creating Graph": 3
}

debugging = False


def main():
    global debugging
    debugging = (input("Running in debug mode (Y/N): ") == "Y")
    for mode in modes:
        print(repr(mode), ":", modes[mode])
    mode_id = int(input("What mode are you running in: "))

    if mode_id == 1:
        if not debugging:
            for league in leagues:
                print(repr(league), ":", leagues[league])
            league_id = int(input("Enter league ID: "))
            teams = get_teams(league_id)
            for team in teams:
                print(repr(teams), ":", teams[team])
            # get teams in that league
            home_team_id = int(input("Enter home team number: "))
            away_team_id = int(input("Enter away team number: "))
            home_team_hashtag = input("Enter home team hashtag: ")
            away_team_hashtag = input("Enter away team hashtag: ")
            neutral_team_hashtag = input("Enter neutral hashtag: ")
        else:
            league_id = 524
            home_team_id = 49
            away_team_id = 52
            home_team_hashtag = "#Chelsea"
            away_team_hashtag = "#Crystal_Palace"
            neutral_team_hashtag = "#CheVSCry"
        # pass hashtags to twitter class that will take care of getting the tweets
        fixture_ID = get_fixtureID(home_team_id, away_team_id, league_id)
        match_events, timestamp = get_match_events(fixture_ID)
        print('python twitter.py ' + home_team_hashtag[1:] + " " + away_team_hashtag[1:] + " " +
                  neutral_team_hashtag[1:] + " " + timestamp)
        os.system('python twitter.py ' + home_team_hashtag[1:] + " " + away_team_hashtag[1:] + " " +
                  neutral_team_hashtag[1:] + " " + timestamp)
    elif mode_id == 2:
        # Trigger analyzer to process tweets that were outputed by the farm
        os.system("python cleanTweets.py")
    elif mode_id == 3:
        os.system("python makeGraph.py")


def get_teams(league_id):
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/" + str(league_id)
    if debugging:
        with open("premteams.json", encoding="utf8") as json_file:
            json_response = json.load(json_file)
    else:
        response = query_api(url)
        json_response = json.load(response)
    teams = {}
    for team in json.response["api"]["teams"]:
        teams[team["name"]] = team["team_id"]
    return teams

def get_fixtureID(home_team_id, away_team_id, league_id):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/" + str(home_team_id) + "/" + str(league_id)

    # Real code
    # response = query_api(url)
    # json_response = json.load(response)

    if debugging:
        with open("fixtureID.json", encoding="utf8") as json_file:
            json_response = json.load(json_file)
    else:
        response = query_api(url)
        json_response = json.load(response)

    for fixture in json_response["api"]["fixtures"]:
        targetFixture_id = 0
        if (fixture["homeTeam"]["team_id"] == home_team_id and fixture["awayTeam"]["team_id"] == away_team_id and
                fixture["league_id"] == league_id and fixture["status"] == "Match Finished"):
            targetFixture_id = fixture["fixture_id"]
            break
        # Error catching stuff should go here.
    return targetFixture_id


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
    timestamp = json.dumps(json_response["api"]["fixtures"][0]["event_timestamp"])
    return match_events, timestamp


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
