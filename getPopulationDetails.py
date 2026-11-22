#this file gets detailed information for population for further processing

import json
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv
API_KEY = os.environ["API_KEY"]

processed = set()

with open("populationData.jsonl", "r", encoding="utf-8") as pdata:
    for line in pdata:
        obj = json.loads(line)
        processed.add(obj["steamId"])


with open("rankings.json", "r", encoding="utf-8") as rankings:
    gameList = json.load(rankings)
steamIds = [game["steamId"] for game in gameList]


# getting info part
failed = []

headers = {"api-key": API_KEY}

with open("populationData.jsonl", "a", encoding="utf-8") as f:
    # for range:
    # day 1 0, 1800 (beause i used ~ 400 today for testing)
    # day 2 1800, len(steamIds) (should be 2340 api calls, under the 2500/day limit)
    for i in range(1800, len(steamIds)):
        response = None
        if steamIds[i] in processed:
            continue   # prevents data corruption if i accidentially run the day 1 range again

        url = f"https://api.gamalytic.com/game/{steamIds[i]}"
        for attempt in range(3):
            
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                break
            if response.status_code != 200:
                print("Error: ", response.status_code, response.text[:200], steamIds[i])

            time.sleep(0.5) #prevent rate limits
            
        if response is None or response.status_code != 200:
            failed.append(steamIds[i])
            continue

        data = response.json()

        f.write(json.dumps(data) + "\n")
        print(f"{steamIds[i]} done")
        processed.add(steamIds[i])

        time.sleep(0.2) #prevent rate limits
        
print(failed)