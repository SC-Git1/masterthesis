import resreg
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from xgboost import DMatrix
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt


def customMSE(dtrain: DMatrix, predt: np.ndarray) -> Tuple[str, float]:

    return mean_squared_error(dtrain, predt)


if __name__ == "__main__":
    # import data
    dfInput = pd.read_csv("All_Input_.tsv", sep="\t", header=0)
    filter_col = [i for i in dfInput.columns if i.endswith("mean")]
    X = dfInput[filter_col]
    y = dfInput["Temp"]

    with open("paramsRF.tsv", 'r') as f:
        lines = f.readlines()
        params = [line.replace("\n", "").split("\t") for line in lines]

    for i in range(1,2):
        random_state = 1
        paramset = params[i]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=random_state)
        X_train, X_valTot, y_train, y_valTot = train_test_split(X_train, y_train, test_size=0.11,
                                                                    random_state=random_state)  # 0.25 x 0.8 = 0.2


        y_valExt = y_valTot[(y_valTot > 40) | (y_valTot < 22)]
        y_mes = y_valTot[(y_valTot < 40) & (y_valTot > 22)]
        minlen = min(len(y_valExt), len(y_mes))
        y_val = pd.concat([y_valExt[0:minlen], y_mes[0:minlen]])
        X_val = X_valTot.loc[y_val.index]

        # read in the hyperparameters from the param file
        print(paramset)
        n_estimators = int(paramset[0])
        max_depth = int(paramset[1])
        min_samples_split = float(paramset[2])
        min_samples_leaf = int(paramset[3])
        ccp_alpha = float(paramset[4])

        # train model
        opt_model = RandomForestRegressor(max_depth=max_depth,
                                          min_samples_split=min_samples_split,
                                          n_estimators=n_estimators,
                                          min_samples_leaf=min_samples_leaf,
                                          ccp_alpha=ccp_alpha)

        opt_model.fit(X_train, y_train)

        # predict on the validation and test data
        y_valpred = opt_model.predict(X_val)
        y_pred = opt_model.predict(X_test)


        # calculate the MSE per bin
        bins = [22, 32, 45, 60]
        mse = mean_squared_error(y_test, y_pred, squared=False)
        msebins = resreg.bin_performance(y_test, y_pred, bins=bins, metric='rmse')

        ## Plot the RMSE per temperature bin
        bin_names = ['<22', '22-32', '32-45', '45-60', '>60']
        plt.bar(range(len(bin_names)), msebins, color = "deepskyblue")
        plt.axhline(mse, color='black', linestyle='--')
        _ = plt.xticks(range(len(bin_names)), bin_names)
        plt.xlabel('Temperature bin [°C]')
        ax = plt.gca()
        ax.margins(y=0.15)
        for bars in ax.containers:
            ax.bar_label(bars, fmt='%.1f', fontsize=9, padding=0, c = "black")
        plt.ylabel('RMSE [°C]')
        plt.title("Random forest", x=0.5, y=0.9, fontdict = {'fontsize' : 11})

        plt.show()


