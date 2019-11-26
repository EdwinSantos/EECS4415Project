#!/usr/bin/python

import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests

def main():
    get_match_events()

def get_match_events():
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/" + str(524)
    response = query_api(url)
    with open('data.json', 'w') as f:
        json.dump(response, f)
    print(response)

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