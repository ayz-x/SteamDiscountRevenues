from scipy import stats
import numpy as np
import pandas as pd

df = pd.read_excel("gameData.xlsx")
data = df["% change"]


def t_Interval(data, confidence):
    n = len(data)
    mean = np.mean(data)
    stdev = np.std(data, ddof=1)
    #ddof is delta degrees of freedom
    alpha = 1 - confidence
    t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
    margin_error = t_crit * (stdev / np.sqrt(n))
    lower = mean - margin_error
    upper = mean + margin_error
    return (lower, upper)


lower = 0
upper = 0
lower, upper = t_Interval(data, 0.99)
print(f"99% CI of %change: ({lower}, {upper})")

lower, upper = t_Interval(data, 0.95)
print(f"95% CI of %change: ({lower}, {upper})")

lower, upper = t_Interval(data, 0.90)
print(f"90% CI of %change: ({lower}, {upper})")

