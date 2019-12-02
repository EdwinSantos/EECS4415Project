#!/usr/bin/python

import json
import os
import requests
import twitter

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

    matches = []
    if mode_id == 1:
        if not debugging:
            while True:
                # Print out list of leagues that can be chosen from. This list can be expanded but it should not be
                # expanded beyond leagues in primarily english speaking countries.
                for league in leagues:
                    print(repr(league), ":", leagues[league])
                league_id = int(input("Enter league ID: "))
                # Get all the teams in that league from the API and let the user pick what teams they are going to use
                teams = get_teams(league_id)
                for team in teams:
                    print(team, ":", teams[team])
                # get teams in that league
                home_team_id = int(input("Enter home team number: "))
                away_team_id = int(input("Enter away team number: "))
                # Prompt the user to enter the hashtags that are used. The last tag can be generated automatically
                # but it is not reliable
                home_team_hashtag = input("Enter home team hashtag with #: ")
                away_team_hashtag = input("Enter away team hashtag with #: ")
                neutral_team_hashtag = input("Enter neutral hashtag with #: ")
                fixture_ID, timestamp = get_fixture_id(home_team_id, away_team_id, league_id)
                save_match_events(fixture_ID)
                matches.append([home_team_hashtag[1:], away_team_hashtag[1:], neutral_team_hashtag[1:], timestamp])
                nextMatch = (input("Add another match? (Y/N): ") == "Y")
                if not nextMatch:
                    break
        else:
            # Values used in debugging mode
            league_id = 524
            home_team_id = 49
            away_team_id = 52
            home_team_hashtag = "#Chelsea"
            away_team_hashtag = "#Crystal_Palace"
            neutral_team_hashtag = "#CheVSCry"
            # get the timestamp and match events

        twitter.build_query(matches)
        # pass hashtags to twitter class that will take care of getting the tweets
        #print('python twitter.py ' + home_team_hashtag[1:] + " " + away_team_hashtag[1:] + " " +
        #      neutral_team_hashtag[1:] + " " + timestamp)
        #os.system('python twitter.py ' + home_team_hashtag[1:] + " " + away_team_hashtag[1:] + " " +
        #          neutral_team_hashtag[1:] + " " + timestamp)
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
        json_response = json.loads(response)
    teams = {}
    # Store the teams in a dictionary because its easy to output this way
    for team in json_response["api"]["teams"]:
        dic_item = [(team["name"], str(team["team_id"]))]
        teams.update(dic_item)
    return teams


def get_fixture_id(home_team_id, away_team_id, league_id):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/" + str(home_team_id) + "/" + str(league_id)

    if debugging:
        with open("fixtureID.json", encoding="utf8") as json_file:
            json_response = json.load(json_file)
    else:
        response = query_api(url)
        json_response = json.loads(response)
    # Get fixture ID this is useful for getting information easier from the API
    for fixture in json_response["api"]["fixtures"]:
        targetFixture_id = 0
        if (fixture["homeTeam"]["team_id"] == home_team_id and fixture["awayTeam"]["team_id"] == away_team_id and
                fixture["league_id"] == league_id):
            targetFixture_id = fixture["fixture_id"]
            timestamp = fixture["event_timestamp"]
            break
    return targetFixture_id, timestamp


def save_match_events(fixture_id):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/id/" + str(fixture_id)
    print(debugging)
    if debugging:
        with open("MatchEvents.json", encoding="utf8") as json_file:
            json_response = json.load(json_file)
    else:
        response = query_api(url)
        json_response = json.loads(response)

    file_name = str(json_response["api"]["fixtures"][0]["fixture_id"]) + ".json"
    with open(file_name, 'w') as outputFile:
        json.dump(json_response["api"]["fixtures"][0], outputFile)

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
