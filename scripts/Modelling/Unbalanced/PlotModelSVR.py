import resreg
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import DMatrix
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import matplotlib.ticker as ticker
from sklearn.inspection import permutation_importance


def customMSE(dtrain: DMatrix, predt: np.ndarray) -> Tuple[str, float]:
    ''' Mean squared error '''
    # actual, predicted
    return mean_squared_error(dtrain, predt)


if __name__ == "__main__":
    dfInput = pd.read_csv("All_Input_.tsv", sep="\t", header=0)
    filter_col = [i for i in dfInput.columns if i.endswith("mean")]
    X = dfInput[filter_col]
    y = dfInput["Temp"]

    # scale the data
    X = pd.DataFrame(StandardScaler().fit_transform(X), )

    # read in the hyperparameters (example file available on GitHub)
    with open("paramsSVR.tsv", 'r') as f:
        lines = f.readlines()
        params = [line.replace("\n", "").split("\t") for line in lines]

    for i in range(1,2):
        random_state = 3
        paramset = params[i]
        print(paramset)

        # split into training, validation and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=random_state)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.11,
                                                                    random_state=random_state)  # 0.25 x 0.8 = 0.2

        # balance the validation set
        y_valExt = y_val[(y_val > 40) | (y_val < 22)]
        y_mes = y_val[(y_val < 40) & (y_val > 22)]
        minlen = min(len(y_valExt), len(y_mes))
        y_val = pd.concat([y_valExt[0:minlen], y_mes[0:minlen]])
        X_val = X_val.loc[y_val.index]

        # set the hyperparameters

        C = float(paramset[0])
        epsilon = float(paramset[1])

        # define and train the SVR model
        opt_model = SVR(kernel = "rbf", C = C, epsilon = epsilon)

        opt_model.fit(X_train, y_train)


        # perform permutation importance
        results = permutation_importance(opt_model, X_test, y_test, scoring='neg_root_mean_squared_error')
        # get importance
        importance = results.importances_mean


        ## plot feature importance
        plt.bar([x for x in range(len(importance))], importance, color = "#8fdbbd")
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.gca().set_xticklabels(['','','','','K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'K10', 'T1', 'T2', 'T3', 'T4', 'T5',
                            'ST1', 'ST2', 'ST3', 'ST4', 'ST5', 'ST6', 'ST7', 'ST8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
                            'B7', 'B8', 'B9', 'B10', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'MSWHIM1', 'MSWHIM2', 'MSWHIM3',
                            'VHSE1', 'VHSE2', 'VHSE3', 'VHSE4', 'VHSE5', 'VHSE6', 'VHSE7', 'VHSE8', 'F1', 'F2', 'F3',
                            'F4', 'F5', 'F6', 'PP1', 'PP2', 'PP3'], rotation=90, fontsize = 9)
        plt.ylabel("Importance score [°C]")
        plt.tight_layout()
        plt.show()

        y_valpred = opt_model.predict(X_val)
        y_pred = opt_model.predict(X_test)

        bins = [22, 32, 45, 60]
        mse = mean_squared_error(y_test, y_pred, squared=False)
        msebins = resreg.bin_performance(y_test, y_pred, bins=bins, metric='rmse')


        ## Plot the RMSE per temperature bin
        bin_names = ['<22', '22-32', '32-45', '45-60', '>60']

        plt.bar(range(len(bin_names)), msebins, color = "deepskyblue")
        plt.axhline(mse, color='black', linestyle='--', lw = 1)
        _ = plt.xticks(range(len(bin_names)), bin_names)
        plt.xlabel('Temperature bin [°C]')

        ax = plt.gca()
        ax.margins(y=0.4)
        for bars in ax.containers:
            ax.bar_label(bars, fmt='%.1f', fontsize=9, padding=6, c = "black")
        plt.ylabel('RMSE [°C]')
        plt.title("SVR", x=0.5, y=0.9, fontdict = {'fontsize' : 11})
        plt.gcf().set_size_inches(5,5)
        plt.show()


        ## plot the measured versus predicted plot for train and test set
        y_predTrain = opt_model.predict(X_train)
        plt.scatter(y_train, y_predTrain, color="navy", s=8, label = "Train")
        plt.scatter(y_test, y_pred, s=8, color="#20bb97", label = "Test")

        p1 = max(max(y_test), max(y_pred), max(y_train), max(y_predTrain))
        p2 = min(min(y_test), min(y_pred), min(y_train), min(y_predTrain))
        plt.plot([p1, p2], [p1, p2], linestyle='-', color="silver")


        plt.axis('equal')
        plt.ylabel("Predicted OGT [°C]")
        plt.xlabel("Measured OGT [°C]")
        plt.legend()
        plt.gcf().set_size_inches(4, 4)
        plt.show()

