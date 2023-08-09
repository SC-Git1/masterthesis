from sklearn.model_selection import cross_val_score
from sklearn.svm import SVR
import pandas as pd
from sklearn.preprocessing import StandardScaler


# import data
df = pd.read_csv("All_Input_.tsv", sep = "\t", header = 0)
filter_col = [i for i in df.columns if i.endswith("mean")]

# extract features and target
X = df[filter_col]
X = pd.DataFrame(StandardScaler().fit_transform(X), )
y = df["Temp"]

# read in the optimal hyperparameters from a tab-delimited file with C followed by epsilon (example available on GitHub)
with open("paramsSVR.tsv", 'r') as f:
    lines = f.readlines()
    params = [line.replace("\n", "").split("\t") for line in lines]

paramset = params[1]
C = float(paramset[0])
epsilon = float(paramset[1])

# Create an SVR model with chosen hyperparameters
opt_model = SVR(kernel='rbf', C=C, epsilon = epsilon)

# Estimate the test error using cross-validation
scores = cross_val_score(opt_model, X, y, cv=10, scoring='neg_root_mean_squared_error')
print(scores)
test_error_estimate = -scores.mean()
print(f"Estimated test error: {test_error_estimate:.4f}")

scores = cross_val_score(opt_model, X, y, cv=10, scoring='r2')
print(scores)
test_error_estimate = -scores.mean()

print(f"Estimated test R²: {test_error_estimate:.4f}")