# add libraries
import requests
import pandas as pd
from pprint import pprint
import time
from helpers import *

# Data Acquisition

# Get API key
filename = '../api'
api_key = get_file_contents(filename)

headers = {}
headers["X-Riot-Token"] = api_key


# League-V4
queue = 'RANKED_SOLO_5x5'
tier = 'DIAMOND'
division = 'I'

params = {
    "page": 1
}

url = 'https://na1.api.riotgames.com/lol/'
league_url = f'{url}league/v4/entries/{queue}/{tier}/{division}'

league_data = []
for i in range(5):
    params["page"] = i + 1
    res = requests.get(url = league_url, params = params, headers = headers)
    league_data.append(res.json())

summoner_ids = []
for page in league_data:
    for entry in page:
        summoner_ids.append(entry.get('summonerId'))


# SUMMONER-V4
summoner_data = []
for id in summoner_ids:
    summoner_url = f'{url}summoner/v4/summoners/{id}'
    res = requests.get(url = summoner_url, headers = headers)
    summoner_data.append(res.json())
    time.sleep(1)

puuids = []
for summoner in summoner_data:
    puuids.append(summoner.get('puuid'))


# MATCH-V5
last_10_games = []

params = {
    "queue": 420,
    "start": -1,
    "count": 11
}

for puuid in puuids:
    last_10_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    res = requests.get(url = last_10_url, params = params, headers = headers)
    for match_id in res.json():
        last_10_games.append(match_id)
    time.sleep(1)

games = []
for match_id in last_10_games:
    match_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    res = requests.get(url = match_url, headers = headers)
    if res.status_code == 200:
        match = res.json()
        if match.get('info').get('frameInterval'):
            game = Game(match)
            games.append(game)
            time.sleep(0.8)
    

games_df = pd.DataFrame([vars(g) for g in games])

games_df_large = games_df.drop_duplicates('id')

games_df_large.to_csv('../data/large_sample.csv')