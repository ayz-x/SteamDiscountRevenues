from scipy import stats
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt







df = pd.read_excel("gameData.xlsx")
x = df[
    ["avgSaleDepth",
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
     ]]

scaler = StandardScaler()
x = scaler.fit_transform(x)
y = df["change"]
y = np.log(y - min(y) + 1)


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


model = ElasticNetCV(
    l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
    cv=5
    )

model.fit(X_train, y_train)


print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)
print("Alpha:", model.alpha_)

# ElasticNetCV only
print("L1 ratio:", model.l1_ratio_)
print("Score:",model.score(X_test,y_test))

y_pred = model.predict(X_train)
residuals = y_pred - y_train



plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Fitted values (predicted y)")
plt.ylabel("Residuals")
plt.title("Residuals vs Fitted Values (Linearity check)")
plt.show()

#with open("elasticNet.txt", "w") as f:
    #f.write(model.summary().as_text())