#first layer of criteria matching, returns a list with basic requirements met

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv
API_KEY = os.environ["API_KEY"]



url = "https://api.gamalytic.com/steam-games/list"
page = 0
gameList = []

while True: 
    params = {
        "page": page,
        "limit": 1000,
        "fields": "steamId,name,copiesSold", 
        "sort": "copiesSold",
        "sort_mode": "desc",
        "release_status": "released",
        "price_min": 0.01,
        "first_release_date_max": 1735689599000, #before 12/31/2024, 11:59:59 PM
        "sold_min": 100000
    }
    headers = {
        "api-key": API_KEY
    }

    response = requests.get(url,params=params,headers=headers)

    print(response.status_code)
    data = response.json()
    

    if not (data): 
        break
    if page == 6:
        break

    games = data["result"]
    gameList.extend(games)  # add this page to master list
    print(f"Page {page} added: {len(data)} games")
    

    page = page + 1

with open("rankings.json", "w", encoding="utf-8") as rankings: 
    json.dump(gameList, rankings, indent=4)