from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


# import the data
# Alternatively: dfInput = pd.read_csv("All_Input_noCCT.tsv", sep ="\t", header = 0)
dfInput = pd.read_csv("All_Input_.tsv", sep ="\t", header = 0)
dfInput = dfInput.sample(frac = 1, random_state=5).reset_index(drop = True)

# define target
y = dfInput["Temp"]

# get RMSE of the null model
predicted = [np.mean(dfInput["Temp"])]*len(y)
print("RMSE = " + str(round(np.sqrt(mean_squared_error(y, predicted)), 3)))

# scale the predictors
filter_col = [col for col in dfInput if col.endswith("mean")]
p = 58
n = len(dfInput)
dfX = dfInput[filter_col]
dfX = pd.DataFrame(StandardScaler().fit_transform(dfX), columns=filter_col)


# Note: alternatively, for Ridge CV:
# reg = RidgeCV(cv=5).fit(dfX, y)

# fit Lasso with cross-validation
reg = LassoCV(cv=5, random_state=1, max_iter=50000).fit(dfX, y)

# get the coefficient of the penalty term
print(reg.alpha_)

# print the descriptors and their coefficients
for i,j in zip(reg.coef_, filter_col):
    print(str(i) + ": " + str(j))


#y_pred = reg.predict(dfX)

# define the data on which to evaluate the model
# Alternatively: dfInput = pd.read_csv("All_Input_noCCT.tsv", sep ="\t", header = 0)
dfEval = pd.read_csv("All_Input_.tsv", sep = "\t", header = 0)
dfEval = dfEval.sample(frac = 1, random_state=5).reset_index(drop = True)
dfX = dfEval[filter_col]
y = dfEval["Temp"]

# get the 5-fold CV score
cv = KFold(n_splits=5, random_state=1, shuffle=True)
scoresRMSE = cross_val_score(reg, dfX, y, scoring='neg_root_mean_squared_error', cv=cv, n_jobs=-1)
scores = cross_val_score(reg, dfX, y, scoring='r2', cv=cv, n_jobs=-1)

# calculate the adjusted R²
Adj_r2 = [1 - (1-score) * (n-1) / (n-p-1) for score in scores]

# print the mean CV R² and RMSE
print(np.mean(Adj_r2))
print(np.mean(scoresRMSE))

