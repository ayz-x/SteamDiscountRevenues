#second layer of filtering to match criteria
import json

games = []
whitelist = []
gameIndex = 0
tagsSet = set()


with open("populationData.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        game = json.loads(line)
        print(game["firstReleaseDate"]-1735689599000)
        if game["firstReleaseDate"] > 1735689599000:
            break

        priceTime = [g["timeStamp"] for g in game["history"]]
        priceHist = [g["price"] for g in game["history"]]
        revenueHist = [g["revenue"] for g in game["history"]]
        tagsSet.update(game["genres"])

        skipBecause100Discount = False
        for price in priceHist:
            if price == 0:
                skipBecause100Discount = True
                break
        if skipBecause100Discount:
            continue    

        undiscountedPrice = []
        undiscountedPrice.append(priceHist[0])
        for i in range(1, len(priceTime)):
            if priceHist[i] < undiscountedPrice[i-1]:
                undiscountedPrice.append(undiscountedPrice[i-1])
            else: undiscountedPrice.append(priceHist[i-1])
            # find maxes so a change in base price won't let past prices
            # look like a discount

        discountCounter = 0
        nonDiscountCounter = 0
        discountRevenue = 0
        nonDiscountRevenue = 0

        for i in range(0, len(priceTime)):
            if priceTime[i] < 1748736000000: # UTC: Monday, June 1, 2026 at 12:00:00 AM
                continue 
            if priceTime[i] > 1780272000000: # UTC: Sunday, June 1, 2025 at 12:00:00 AM
                break

            if priceHist[i] < undiscountedPrice[i]:
                discountCounter = discountCounter + 1
                discountRevenue = discountRevenue + (revenueHist[i] - revenueHist[i-1])
            if priceHist[i] == undiscountedPrice[i]:
                nonDiscountCounter = nonDiscountCounter + 1
                nonDiscountRevenue = nonDiscountRevenue + (revenueHist[i] - revenueHist[i-1])

        if discountCounter > 59 and nonDiscountCounter > 59 and discountRevenue > 0 and nonDiscountRevenue > 0:
            
            whitelist.append(game)


with open("filteredPData.jsonl", "w", encoding="utf-8") as f: 
    for game in whitelist:
        f.write(json.dumps(game) + "\n")

tagsList = list(tagsSet)
tagsList.sort()

for tag in tagsList:
    print(f"\"{tag}\": [],")