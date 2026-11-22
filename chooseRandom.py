#this file is for sampling.
import json
import random

# population N is 2842
games = []
with open("filteredPData.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        games.append(json.loads(line))

random.seed(42) #to be consistent if rerunning project

sampleList = random.sample(games, 280)

with open("data.jsonl", "w", encoding="utf-8") as f: 
    for game in sampleList:
        f.write(json.dumps(game) + "\n")
    