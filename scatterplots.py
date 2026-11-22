import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


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
x = df[vars]

y = df["change"]
shift = -min(y) + 1
logY = np.log(y + shift)




  
#residuals = y - y_pred

#plt.scatter(df[var], residuals, alpha=0.5)
#plt.axhline(0, color='red', linestyle='--', linewidth=1)
#plt.set_xlabel(var)
#plt.set_ylabel("Residuals")
#plt.set_title(f"Residuals vs {var}")

plt.tight_layout()
plt.show()