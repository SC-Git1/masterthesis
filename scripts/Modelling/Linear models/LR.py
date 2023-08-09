from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# import the data
dfInput = pd.read_csv("All_Input_.tsv", sep ="\t", header = 0)
y = dfInput["Temp"]
predicted = [np.mean(dfInput["Temp"])]*len(y)
print("RMSE = " + str(round(np.sqrt(mean_squared_error(y, predicted)), 3)))

# define descriptors sets and their length
descriptors = ["VHSE", "MSWHIM", "PP", "Z", "ST", "T", "K", "F", "B"]
ps = [8,3,3,5,8,5,10,6,10]

# initialize the R² and RMSE vectors
AlladjR2 = []
AllRMSE = []

## for each descriptor
for i in range(len(descriptors)):
    ## define input and variables
    short = descriptors[i]
    # number of components in descriptor set
    p = ps[i]
    # number of observations
    n = len(dfInput)
    file = short
    filter_col = [col for col in dfInput if col.startswith(short) and col.endswith("mean")]
    dfX = dfInput[filter_col]

    # calculate the 5-fold CV R² and RMSE with standard linear regression
    estimator = LinearRegression()
    cv = KFold(n_splits=5, random_state=1, shuffle=True)
    scores = cross_val_score(estimator, dfX, y, scoring='r2', cv=cv, n_jobs=-1)
    Adj_r2 = [1 - (1-score) * (n-1) / (n-p-1) for score in scores]
    scoresRMSE = cross_val_score(estimator, dfX, y, scoring='neg_root_mean_squared_error', cv=cv, n_jobs=-1)
    # append
    AlladjR2.append(Adj_r2)
    AllRMSE.append(scoresRMSE*-1)

# transpose because now 5 columns
columns = ["VHSE", "MS-WHIM", "PP", "Z-scales", "ST-scales", "T-scales", "Kidera", "FASGAI", "Blosum"]
adjR2 = pd.DataFrame([list(i) for i in zip(*AlladjR2)], columns=columns)
adjR2["id"] = adjR2.index
adjR2 = pd.melt(adjR2, id_vars=['id'], value_vars=columns)

RMSE = pd.DataFrame([list(i) for i in zip(*AllRMSE)], columns=columns)
RMSE["id"] = RMSE.index
RMSE = pd.melt(RMSE, id_vars=['id'], value_vars=columns)



### plot the adjusted R²

sns.catplot(data=adjR2, x="variable", y="value", capsize=.2, color="forestgreen",
errorbar="se", kind="point", aspect=.75, join=False, scale=0.45,
errwidth=0.9, height = 3)
plt.xlabel("")
plt.xticks(rotation = 90)
plt.ylabel("Adjusted R²")
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
plt.tight_layout()
plt.gcf().set_size_inches(5,3.75)
plt.show()

## plot the RMSE
sns.catplot(data=RMSE, x="variable", y="value", capsize=.2, color="darkorchid",
errorbar="se", kind="point", aspect=.75, join=False, scale=0.45,
errwidth=0.9, height = 3)
plt.xlabel("")
plt.xticks(rotation = 90)
plt.ylabel("RMSE [°C]")
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
plt.tight_layout()
plt.gcf().set_size_inches(5,3.75)
plt.show()


