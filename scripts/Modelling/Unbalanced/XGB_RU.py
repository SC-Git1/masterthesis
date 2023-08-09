import numpy as np
from typing import Tuple
import pandas as pd
import optuna
from xgboost import XGBRegressor, DMatrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error



def objective(trial):

    def customMSE(dtrain: DMatrix, predt: np.ndarray) -> Tuple[str, float]:
        ''' Mean squared error '''
        # actual, predicted
        return mean_squared_error(dtrain, predt)


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

    # initial XGBoost model for this trial
    optuna_model = XGBRegressor(**params)

    # fit
    optuna_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)], verbose = False)
    # note: early_stopping_rounds` in `fit` method is deprecated for better compatibility with scikit-learn, use
    # `early_stopping_rounds` in constructor or`set_params` instead.

    # Make predictions
    y_pred = optuna_model.predict(X_val)

    accuracy = customMSE(y_val, y_pred)
    return accuracy


if __name__ == "__main__":

    ## Import data
    dfInput = pd.read_csv("All_Input_.tsv", sep="\t", header=0)
    filter_col = [i for i in dfInput.columns if i.endswith("mean")]
    X = dfInput[filter_col]
    y = dfInput["Temp"]

    # open output file
    with open("XGB_Random.tsv", mode="a") as f:
        f.write("random_state" + "\t" + "C" + "\t" + "epsilon" + "\t" + "TestR2" + "\t" + "TestRMSE" + "\t" +
                "ValR2" + "\t" + "ValRMSE" + "\t" + "TrainR2" + "\t" + "TrainRMSE" + "\n")

        for random_state in range(1, 11):
            # split into training, test and validation set
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=random_state)
            X_train, X_valTot, y_train, y_valTot = train_test_split(X_train, y_train, test_size=0.11,
                                                              random_state=random_state)  # 0.25 x 0.8 = 0.2


            # balance the validation set
            y_valExt = y_valTot[(y_valTot > 40) | (y_valTot < 22)]
            y_mes = y_valTot[(y_valTot < 40) & (y_valTot > 22)]
            minlen = min(len(y_valExt), len(y_mes))
            y_val = pd.concat([y_valExt[0:minlen], y_mes[0:minlen]])
            X_val = X_valTot.loc[y_val.index]

            study = optuna.create_study(direction="minimize", sampler=optuna.samplers.RandomSampler(seed = random_state)) # maximise the score during tuning

            study.optimize(objective, n_trials=100)
            # print some stuff

            # select the hyperparameters of the best trial
            trial = study.best_trial
            opt_params = trial.params

            # define and train the model with the optimal hyperparameters
            opt_model = XGBRegressor(max_depth = opt_params.get("max_depth"), learning_rate  = opt_params.get("learning_rate"),
                                     n_estimators = opt_params.get("n_estimators"), min_child_weight = opt_params.get("min_child_weight"),
                                     gamma = opt_params.get("gamma"), subsample = opt_params.get("subsample"),
                                     reg_lambda = opt_params.get("reg_lambda"), eval_metric = opt_params.get("eval_metric"),
                                     colsample_bylevel = opt_params.get("colsample_bylevel"), seed = 5, early_stopping_rounds = 10)

            opt_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)],
                             verbose=False)

            # get the R² and RMSE scores on the test, training and validation set for the final hyperparameter set
            TestR2 = r2_score(y_test, opt_model.predict(X_test))
            ValR2 = r2_score(y_valTot, opt_model.predict(X_valTot))
            TrainR2 = r2_score(y_train, opt_model.predict(X_train))
            TestRMSE = mean_squared_error(y_test, opt_model.predict(X_test), squared=False)
            ValRMSE = mean_squared_error(y_valTot, opt_model.predict(X_valTot), squared = False)
            TrainRMSE = mean_squared_error(y_train, opt_model.predict(X_train), squared=False)

            # write to file
            f.write(str(random_state) + "\t" + str(opt_params.get("max_depth")) + "\t" + str(opt_params.get("learning_rate")) +
                    "\t" + str(opt_params.get("n_estimators")) + "\t" + str(opt_params.get("min_child_weight")) +
                    "\t" + str(opt_params.get("gamma")) + "\t" + str(opt_params.get("subsample")) + "\t" +
                    str(opt_params.get("reg_lambda")) + "\t" + str(TestR2) + "\t" + str(TestRMSE) + "\t" + str(ValR2) +
                    "\t" + str(ValRMSE) + "\t" + str(TrainR2) + "\t" + str(TrainRMSE) + "\n")
            f.flush()



