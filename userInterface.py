import sys
import requests
import json

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


def main():
    for team in teams:
        print(repr(team), ":", teams[team])
    home_team_id = input("Enter home team number: ")
    away_team_id = input("Enter home team number: ")
    date = input("Enter date of game (YYYYMMDD): ")
    home_team_hashtag = input("Enter home team hashtag: ")
    away_team_hashtag = input("Enter away team hashtag: ")
    neutral_team_hashtag = input("Enter neutral hashtag: ")

    # pass hashtags to other class
    fixture_ID = get_fixtureID(home_team_id, away_team_id, date)
    # get_match_events(fixture_ID)


def get_fixtureID(home_team_id, away_team_hashtag, date):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/" + str(home_team_id) + "/" + str(league_id)
    # debug code

    #Debug code
    with open("fixtureID.json") as json_file:
        json_response = json.load(json_file)
    #end of debug code
    # Real code
    # response = query_api(url)
    #json_response = json.load(response)

    for fixture in json_response["api"]["fixtures"]:
        print(fixture)
    return 34


def get_match_events(date):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/524"
    query_api(url)
    return


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
