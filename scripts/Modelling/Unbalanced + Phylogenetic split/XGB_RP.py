### NOTE: look first at all -> same important as in linear? Then, maybe do some selection of AA descriptors (or of features)
import time
import numpy as np
from typing import Tuple
import pandas as pd
import optuna
from xgboost import XGBRegressor, DMatrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import dendropy
from phylodm import PhyloDM
from sklearn.cluster import AgglomerativeClustering
from itertools import groupby

### Note on data processing:
# how to handle genomes awith multiple accession (just find the average for each accession, now that these are just noise then or
# some duplication :) ALTERNATIVELY, keep each genome separate (but this will further increase the data imbalance since
#  mesophilic organisms are likely to have more genomes => check the average number of genomes per temperature !!!))).
#  For each PAIR of average genome & ncbiTaxID, we can then find the average temp. The input datapoints are then these.

def objective(trial):

    def customMSE(dtrain: DMatrix, predt: np.ndarray) -> Tuple[str, float]:
        ''' Mean squared error '''
        # actual, predicted
        return mean_squared_error(dtrain, predt)

    # define the hyperparameter space
    params = {
        'max_depth': trial.suggest_int('max_depth', 1, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
        'n_estimators': trial.suggest_int('n_estimators', 50, 400),
        'min_child_weight': trial.suggest_int('min_child_weight', 15, 100),
        'gamma': trial.suggest_float('gamma', 1e-8, 10, log=True),
        'subsample': trial.suggest_float('subsample', 0.01, 0.2, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 5.0, log=True),
        'eval_metric': customMSE,
        'seed' : 5,
        'tree_method' : 'gpu_hist',
        'gpu_id' : 0,
        'n_jobs': -1,
        'early_stopping_rounds' : 10
    }


    # initialize and fit the XGBoost model with the hyperparameter of this trial
    optuna_model = XGBRegressor(**params)

    optuna_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)], verbose = False)

    # Make predictions
    y_pred = optuna_model.predict(X_val)

    accuracy = customMSE(y_val, y_pred)
    return accuracy


if __name__ == "__main__":

    ## import data
    dfInput = pd.read_csv("All_Input_.tsv", sep="\t", header=0, dtype = {"ncbiTaxID":str})
    # dfInput = dfInput.sample(frac = 1, random_state=0).reset_index(drop = True)
    filter_col = [i for i in dfInput.columns if i.endswith("mean")]

    # open the output file
    with open("SVR_TPE_PS.tsv", mode="a") as f:
        # write the header
        f.write("random_state" + "\t" + "C" + "\t" + "epsilon" + "\t" + "TestR2" + "\t" + "TestRMSE" + "\t" +
                "ValR2" + "\t" + "ValRMSE" + "\t" + "TrainR2" + "\t" + "TrainRMSE" + "\n")


        for random_state in range(0, 10):
            # Agglomerative clustering with n_clusters = 10 returns labels 0-9.
            # Assign one to the test set and another to the validation set
            testSt = random_state
            if testSt == 9:
                valSt = 0
            else: valSt = random_state+1

            # assign the remaining labels to the training set
            trainSt = [i for i in list(range(0,10)) if i != testSt and i != valSt]

            # load the tree
            tree = dendropy.Tree.get_from_path("TreeProteomes.nw", schema="newick")
            # calculate the distance matrix
            pdm = PhyloDM.load_from_dendropy(tree)
            dm = pdm.dm(norm=False)

            # perform agglomerative clustering
            model = AgglomerativeClustering(affinity='precomputed', n_clusters=10, linkage='complete').fit(dm)
            a = model.labels_
            b = [len(list(group)) for key, group in groupby(sorted(a))]
            labels = pdm.taxa()

            # croeate the test, training and validation set
            TestIdx = [i for i in list(range(len(a))) if a[i] in [testSt]]
            ValidationIdx = [i for i in list(range(len(a))) if a[i] in [valSt]]
            TrainIdx = [i for i in list(range(len(a))) if a[i] in trainSt]


            TestIDs = [labels[i] for i in TestIdx]
            ValidationIDs = [labels[i] for i in ValidationIdx]
            TrainIDs = [labels[i] for i in TrainIdx]

            dfTrain = dfInput[dfInput["ncbiTaxID"].isin(TrainIDs)]
            dfTest = dfInput[dfInput["ncbiTaxID"].isin(TestIDs)]
            dfValidation = dfInput[dfInput["ncbiTaxID"].isin(ValidationIDs)]

            # define the predictors, work with means
            X_train = dfTrain[filter_col]
            X_test = dfTest[filter_col]
            X_val = dfValidation[filter_col]

            # define the targets
            y_train = dfTrain["Temp"]
            y_test = dfTest["Temp"]
            y_val = dfValidation["Temp"]

            # balance the validation set
            y_valExt = y_val[(y_val > 40) | (y_val < 22)]
            y_mes = y_val[(y_val < 40) & (y_val > 22)]
            minlen = min(len(y_valExt), len(y_mes))
            print(minlen)
            y_val = pd.concat([y_valExt[0:minlen], y_mes[0:minlen]])
            X_val = X_val.loc[y_val.index]


            # initialize and start the optimization with Optuna
            study = optuna.create_study(direction = "minimize", sampler=optuna.samplers.TPESampler(seed=random_state)) # maximise the score during tuning

            study.optimize(objective, n_trials=100) # run the objective function 100 times: # ,callbacks=[neptune_callback]

            # get the hyperparameters of the best trial
            trial = study.best_trial
            opt_params = trial.params

            # define and train the XGBoost model with the best hyperparameters found in this trial
            opt_model = XGBRegressor(max_depth = opt_params.get("max_depth"), learning_rate  = opt_params.get("learning_rate"),
                                     n_estimators = opt_params.get("n_estimators"), min_child_weight = opt_params.get("min_child_weight"),
                                     gamma = opt_params.get("gamma"), subsample = opt_params.get("subsample"),
                                     reg_lambda = opt_params.get("reg_lambda"), eval_metric = opt_params.get("eval_metric"),
                                     colsample_bylevel = opt_params.get("colsample_bylevel"), seed = 5, early_stopping_rounds = 10)

            opt_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)],
                             verbose=False)

            # calculate the R² and RMSE on the training, test and validation set
            TestR2 = r2_score(y_test, opt_model.predict(X_test))
            ValR2 = r2_score(y_val, opt_model.predict(X_val))
            TrainR2 = r2_score(y_train, opt_model.predict(X_train))
            TestRMSE = mean_squared_error(y_test, opt_model.predict(X_test), squared=False)
            ValRMSE = mean_squared_error(y_val, opt_model.predict(X_val), squared = False)
            TrainRMSE = mean_squared_error(y_train, opt_model.predict(X_train), squared=False)

            f.write(str(random_state) + "\t" + str(opt_params.get("max_depth")) + "\t" + str(opt_params.get("learning_rate")) +
                    "\t" + str(opt_params.get("n_estimators")) + "\t" + str(opt_params.get("min_child_weight")) +
                    "\t" + str(opt_params.get("gamma")) + "\t" + str(opt_params.get("subsample")) + "\t" +
                    str(opt_params.get("reg_lambda")) + "\t" + str(TestR2) + "\t" + str(TestRMSE) + "\t" + str(ValR2) +
                    "\t" + str(ValRMSE) + "\t" + str(TrainR2) + "\t" + str(TrainRMSE) + "\n")
            f.flush()





