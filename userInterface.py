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


    # Replace this with a list of teams taken from the API
    for team in teams:
        print(repr(team), ":", teams[team])
    home_team_id = int(input("Enter home team number: "))
    away_team_id = int(input("Enter away team number: "))
    home_team_hashtag = input("Enter home team hashtag: ")
    away_team_hashtag = input("Enter away team hashtag: ")
    neutral_team_hashtag = input("Enter neutral hashtag: ")

    # pass hashtags to twitter class that will take care of getting the tweets
    fixture_ID, timestamp = get_fixtureID(home_team_id, away_team_id)
    match_events = get_match_events(fixture_ID)
    # pass events and tweet ratings to class that will make the graph


def get_fixtureID(home_team_id, away_team_id):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/" + str(home_team_id) + "/" + str(league_id)
    
    # Real code
    # response = query_api(url)
    #json_response = json.load(response)
    
    #Debug code
    with open("fixtureID.json", encoding="utf8") as json_file:
        json_response = json.load(json_file)

    for fixture in json_response["api"]["fixtures"]:
        targetFixture_id = 0
        if(fixture["homeTeam"]["team_id"] == home_team_id and fixture["awayTeam"]["team_id"] == away_team_id and
           fixture["league_id"] == 524 and fixture["status"] == "Match Finished"):
            targetFixture_id = fixture["fixture_id"]
            timestamp = fixture["event_date"]
            break
        # Error catching stuff should go here.
    return targetFixture_id, timestamp


def get_match_events(fixture_ID):
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/id/" + str(fixture_ID)
    
    ##Real code
    #response = query_api(url)
    #json_response = json.load(response)

    #Debugging code
    with open("MatchEvents.json", encoding="utf8") as json_file:
        json_response = json.load(json_file)

    match_events = json_response["api"]["fixtures"][0]["events"]
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
