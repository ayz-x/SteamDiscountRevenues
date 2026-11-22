import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew, kurtosis


df = pd.read_excel("gameData.xlsx")
vars = [
    "avgSaleDepth",
    "saleFrequency",
    "releaseDateTimeStamp(ms)",
    "reviews",
    "reviewScore",
    "avgPlaytime",
    "priceBeforeDiscount",
    "wishlists",
    "owners",
    "avgDailyActive",
    "Action",
    "Adventure",
    "Casual",
    "Early Access",
    "Indie",
    "Massively Multiplayer",
    "RPG",
    "Racing",
    "Simulation",
    "Sports",
    "Strategy"
    ]
y = df["change"]
shift = -min(y) + 1
logY = np.log(y + shift)




plt.hist(y, bins=50)
plt.ylabel("freq")
plt.xlabel("percent change in revenue after discount")
L, U = 769.8, 1387.6
plt.axvspan(L, U, color='green', alpha=0.5, label='99% t-interval')
plt.legend()
plt.show()

print(f"Count:              {len(y)}")
print(f"Mean:               {np.mean(y):.4f}")
print(f"Median:             {np.median(y):.4f}")
print(f"Standard deviation: {np.std(y, ddof=1):.4f}")
print(f"Variance:           {np.var(y, ddof=1):.4f}")
print(f"Minimum:            {np.min(y):.4f}")
print(f"25th percentile:    {np.percentile(y, 25):.4f}")
print(f"75th percentile:    {np.percentile(y, 75):.4f}")
print(f"Maximum:            {np.max(y):.4f}")
print(f"Range:              {(np.max(y) - np.min(y)):.4f}")
print(f"IQR:                {(np.percentile(y, 75) - np.percentile(y, 25)):.4f}")
print(f"Skewness:           {skew(y, bias=False):.4f}")