#this file is used to process raw data into a dictionary of lists, or excel

import json
import pandas as pd
from datetime import datetime

games = []
whitelist = []
gameIndex = 0
gameData = {
    "name": [],
    "id": [],
    "change": [],
    "avgSaleDepth": [],
    "saleFrequency": [],
    "releaseDateTimeStamp(ms)": [],
    "releaseDate": [],
    "reviews": [],
    "reviewScore": [],
    "avgPlaytime": [],
    "priceBeforeDiscount": [],
    "wishlists": [],
    "owners": [],
    "avgDailyActive": []
}
gameGenres = {
    "Action": [],
    "Adventure": [],
    "Casual": [],
    "Early Access": [],
    "Indie": [],
    "Massively Multiplayer": [],
    "RPG": [],
    "Racing": [],
    "Simulation": [],
    "Sports": [],
    "Strategy": []
}
genres = ["Action", "Adventure", "Casual", "Early Access",
          "Indie", "Massively Multiplayer", "RPG", "Racing",
          "Simulation", "Sports", "Strategy"]
# 424 tags is too much to manage multicollinearity
# also some tags are too niche and will not be good descriptors
# also 424 dummy variables will probably fry my laptop
# so i changed it to genres, which are more distinct
# see tags.json for all the tags if you're curious

with open("data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        game = json.loads(line)
        priceTime = [g["timeStamp"] for g in game["history"]]
        priceHist = [g["price"] for g in game["history"]]
        revenueHist = [g["revenue"] for g in game["history"]]
        playerHist = [g["players"] for g in game["history"]]

        undiscountedPrice = []
        undiscountedPrice.append(priceHist[0])
        for i in range(1, len(priceTime)):
            if priceHist[i] < undiscountedPrice[i-1]:
                undiscountedPrice.append(undiscountedPrice[i-1])
            else: undiscountedPrice.append(priceHist[i-1])
            # find maxes so a change in base price won't let past prices
            # look like a discount

        discountRevenue = 0
        nondiscountRevenue = 0
        discountCounter = 0
        nonDiscountCounter = 0
        saleDepth = 0
        dailyActive = 0

        for i in range(0, len(priceTime)):
            if priceTime[i] < 1748736000000: # UTC: Monday, June 1, 2025 at 12:00:00 AM
                continue 
            if priceTime[i] > 1780272000000: # UTC: Sunday, June 1, 2026 at 12:00:00 AM
                break
            #this ensures we only collect data for the past year

            dailyActive = dailyActive + playerHist[i]

            if priceHist[i] < undiscountedPrice[i]:
                discountCounter = discountCounter + 1
                discountRevenue = discountRevenue + (revenueHist[i] - revenueHist[i-1])
                saleDepth = saleDepth + ((priceHist[i]-undiscountedPrice[i])/undiscountedPrice[i])*100
            if priceHist[i] == undiscountedPrice[i]:
                nonDiscountCounter = nonDiscountCounter + 1
                nondiscountRevenue = nondiscountRevenue + (revenueHist[i] - revenueHist[i-1])

        saleDepth = saleDepth/discountCounter
        saleFrequency = discountCounter/(discountCounter + nonDiscountCounter)
        dailyRevenue = nondiscountRevenue/nonDiscountCounter
        dailyDiscountRevenue = discountRevenue/discountCounter
        dailyActive = dailyActive/(discountCounter + nonDiscountCounter)

        percentChange = ((dailyDiscountRevenue - dailyRevenue)/dailyRevenue)*100
        gameData["name"].append(game["name"])
        gameData["id"].append(game["steamId"])
        gameData["change"].append(percentChange)
        gameData["avgSaleDepth"].append(saleDepth)
        gameData["saleFrequency"].append(saleFrequency)
        gameData["releaseDateTimeStamp(ms)"].append(game["firstReleaseDate"])
        gameData["releaseDate"].append(datetime.fromtimestamp(game["firstReleaseDate"]/1000).isoformat())
        gameData["reviews"].append(game["reviews"])
        gameData["reviewScore"].append(game["reviewScore"])
        gameData["avgPlaytime"].append(game["avgPlaytime"])
        gameData["priceBeforeDiscount"].append(game["price"])
        gameData["wishlists"].append(game["wishlists"])
        gameData["owners"].append(game["owners"])
        gameData["avgDailyActive"].append(dailyActive)
        
        for i, genre in enumerate(genres):
            if genre in game["genres"]:
                gameGenres[genre].append(1)
            else:
                gameGenres[genre].append(0)

            



        gameIndex = gameIndex + 1
        
gameData.update(gameGenres)
df = pd.DataFrame(gameData)
df.to_excel("gameData.xlsx", index = False)

with open("gameData.json", "w", encoding="utf-8") as f: 
    json.dump(gameData, f, indent=4)
    




        