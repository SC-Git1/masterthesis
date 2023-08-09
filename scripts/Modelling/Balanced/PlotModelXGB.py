import resreg
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import XGBRegressor, DMatrix
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt



def customMSE(dtrain: DMatrix, predt: np.ndarray) -> Tuple[str, float]:
    ''' Mean squared error '''
    # actual, predicted
    return mean_squared_error(dtrain, predt)


if __name__ == "__main__":
    # import data
    dfInput = pd.read_csv("All_Input_.tsv", sep="\t", header=0)
    random_state = 8
    dfInput = dfInput.sample(frac=1, random_state=random_state).reset_index()

    # define the predictors and the target
    Xcols = [i for i in dfInput.columns if i.endswith("_mean")]
    dfX = dfInput[Xcols]
    dfY = dfInput["Temp"]

    # read in the hyperparameters
    with open("params.tsv", 'r') as f:
        lines = f.readlines()
        params = [line.replace("\n", "").split("\t") for line in lines]

    for i in range(1,2):
        random_state = 3
        paramset = params[i]

        # create the uniform test set
        bins = [22, 32, 45, 60]

        train_indices, test_indices = resreg.uniform_test_split(dfX, dfY, bins=bins,
                                                                bin_test_size=0.5, verbose=True,
                                                                random_state=random_state)

        X_train, y_train = dfX.iloc[train_indices, :], dfY[train_indices]
        X_test, y_test = dfX.iloc[test_indices, :], dfY[test_indices]
        print(f'Training set has {len(y_train)} samples')
        print(f'Testing set has {len(y_test)} samples')


        # create the training and test set
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25,
                                                          random_state=random_state)  # 0.25 x 0.8 = 0.2

        # define the relavance function
        relevance = resreg.sigmoid_relevance(y_train, cl=22, ch=40)


        ### Note: comment out for one of the resampling methods
        ## use random undersampling
        X_train, y_train = resreg.random_undersample(X_train, y_train, relevance, relevance_threshold=0.5,
                                                    under='average', random_state=random_state)

        #X_train, y_train = resreg.smoter(X_train, y_train, relevance, relevance_threshold=0.5, k=5,
        #                                 over="balance", random_state=random_state)

        #X_train, y_train = resreg.gaussian_noise(X_train, y_train, relevance,
        #                                         relevance_threshold=0.5, over="average", random_state=random_state)

        # rename the columns
        X_train = pd.DataFrame(X_train, columns=X_val.columns)
        y_train = pd.DataFrame(y_train, columns=["Temp"])


        # balance the validation set
        y_ExtIdx = list(np.where((y_val > 40) | (y_val < 22))[0])
        print(y_ExtIdx)
        y_val = y_val.iloc[y_ExtIdx]
        X_val = X_val.iloc[y_ExtIdx]
        print(len(y_val))

        # get the hyperparameters:

        max_depth = int(paramset[0])
        learning_rate = float(paramset[1])
        n_estimators = int(paramset[2])
        min_child_weight = int(paramset[3])
        gamma = float(paramset[4])
        subsample = float(paramset[5])
        reg_lambda = float(paramset[6])


        # define the XGBoost model using the optimal hyperparameters and fit
        opt_model = XGBRegressor(max_depth = max_depth, learning_rate  = learning_rate, n_estimators = n_estimators,
                                 min_child_weight = min_child_weight, gamma = gamma, subsample = subsample,
                                 reg_lambda = reg_lambda, seed = random_state, early_stopping_rounds = 10)


        opt_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)], verbose=False)

        # calculate the training, validation and test set R² and RMSE
        TestR2 = r2_score(y_test, opt_model.predict(X_test))
        ValR2 = r2_score(y_val, opt_model.predict(X_val))
        TrainR2 = r2_score(y_train, opt_model.predict(X_train))
        TestRMSE = mean_squared_error(y_test, opt_model.predict(X_test), squared=False)
        ValRMSE = mean_squared_error(y_val, opt_model.predict(X_val), squared=False)
        TrainRMSE = mean_squared_error(y_train, opt_model.predict(X_train), squared=False)

        # calculate and plot the RMSE per temperature bin
        y_pred = opt_model.predict(X_test)
        bins = [22, 32, 45, 60]
        mse = mean_squared_error(y_test, y_pred, squared=False)
        msebins = resreg.bin_performance(y_test, y_pred, bins=bins, metric='rmse')

        # Plot MSE
        bin_names = ['<22', '22-32', '32-45', '45-60', '>60']
        plt.bar(range(len(bin_names)), msebins, color = "deepskyblue")
        plt.axhline(mse, color='black', linestyle='--')
        _ = plt.xticks(range(len(bin_names)), bin_names)
        plt.xlabel('Bins of temperatures [°C]')
        # Add label on top of each bar
        ax = plt.gca()
        ax.margins(y=0.3)  # make room for the labels
        for bars in ax.containers:
            ax.bar_label(bars, fmt='%.1f', fontsize=9, padding=0, c = "black")

        plt.ylabel('RMSE [°C]')
        plt.title("XGBoost - Undersampling", x=0.5, y=0.9, fontdict = {'fontsize' : 11})

        plt.show()
        plt.close()

