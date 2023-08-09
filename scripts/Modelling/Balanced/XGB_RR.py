import numpy as np
from typing import Tuple
import pandas as pd
import optuna
from xgboost import XGBRegressor, DMatrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import resreg
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


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

    optuna_model = XGBRegressor(**params)

    optuna_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)], verbose = False)

    # Make predictions
    y_pred = optuna_model.predict(X_val)

    accuracy = customMSE(y_val, y_pred)
    return accuracy


if __name__ == "__main__":

    # import data
    dfInput = pd.read_csv("All_Input_.tsv", sep="\t", header=0)
    random_state = 8
    dfInput = dfInput.sample(frac=1, random_state=random_state).reset_index()

    # define predictors and target
    Xcols = [i for i in dfInput.columns if i.endswith("_mean")]
    dfX = dfInput[Xcols]
    dfY = dfInput["Temp"]
    print(dfY)

    # open output file
    with open("XGB_US_CORRECT.tsv", mode="a") as f:
        f.write("random_state" + "\t" + "random_state" + "\t" + "max_depth" + "\t" + "learning_rate" + "\t" +
          + "n_estimators" + "\t" + "min_child_weight" + "\t"	+ "gamma" + "\t" + "subsample" + "\t" +	"reg_lambda" + "\n")

        for random_state in range(1,11):
            # define bins for creation of the uniform test set
            bins = [22, 32, 45, 60]

            train_indices, test_indices = resreg.uniform_test_split(dfX, dfY, bins=bins,
                                                                    bin_test_size=0.5, verbose=True,
                                                                    random_state=random_state)

            X_train, y_train = dfX.iloc[train_indices, :], dfY[train_indices]
            X_test, y_test = dfX.iloc[test_indices, :], dfY[test_indices]

            # create validation and training set
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25,
                                                              random_state=random_state)  # 0.25 x 0.8 = 0.2

            # define relevance function
            relevance = resreg.sigmoid_relevance(y_train, cl=22, ch=40)


            ### use resampling, comment out the appropriate section
            # section1: random undersampling
            X_train, y_train = resreg.random_undersample(X_train, y_train, relevance, relevance_threshold=0.5,
                                                        under='average', random_state=random_state)
            # section2: SMOTER
            X_train, y_train = resreg.smoter(X_train, y_train, relevance,
                          relevance_threshold=0.5, k=5, over="balance", random_state=random_state)

            # section: GN
            X_train, y_train = resreg.gaussian_noise(X_train, y_train, relevance,
                      relevance_threshold=0.5, over="average", random_state=random_state)


            # rename the columns
            X_train = pd.DataFrame(X_train, columns=X_val.columns)
            y_train = pd.DataFrame(y_train, columns=["Temp"])


            # balance the validation set
            y_ExtIdx = list(np.where((y_val > 40) | (y_val < 22))[0])
            print(y_ExtIdx)
            y_val = y_val.iloc[y_ExtIdx]
            X_val = X_val.iloc[y_ExtIdx]
            print(len(y_val))

            # define and start the Optuna optimization
            study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=random_state)) # maximise the score during tuning

            study.optimize(objective, n_trials=100)
            # study.optimize(objective, n_trials=100,callbacks=[neptune_callback]) # run the objective function 100 times: # ,callbacks=[neptune_callback]

            # extract the best hyperparameters
            trial = study.best_trial
            opt_params = trial.params

            ## define and train the XGBoost model on the optimized hyperparameters
            opt_model = XGBRegressor(max_depth = opt_params.get("max_depth"), learning_rate  = opt_params.get("learning_rate"),
                                     n_estimators = opt_params.get("n_estimators"), min_child_weight = opt_params.get("min_child_weight"),
                                     gamma = opt_params.get("gamma"), subsample = opt_params.get("subsample"),
                                     reg_lambda = opt_params.get("reg_lambda"), eval_metric = opt_params.get("eval_metric"),
                                     seed = random_state, early_stopping_rounds = 10)

            opt_model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)], verbose=False)

            # calculate the R² and RMSE on the training, test and validation set
            TestR2 = r2_score(y_test, opt_model.predict(X_test))
            ValR2 = r2_score(y_val, opt_model.predict(X_val))
            TrainR2 = r2_score(y_train, opt_model.predict(X_train))
            TestRMSE = mean_squared_error(y_test, opt_model.predict(X_test), squared=False)
            ValRMSE = mean_squared_error(y_val, opt_model.predict(X_val), squared = False)
            TrainRMSE = mean_squared_error(y_train, opt_model.predict(X_train), squared=False)


            # write to the output file
            f.write(str(random_state) + "\t" + str(opt_params.get("max_depth")) + "\t" + str(opt_params.get("learning_rate")) +
                    "\t" + str(opt_params.get("n_estimators")) + "\t" + str(opt_params.get("min_child_weight")) +
                    "\t" + str(opt_params.get("gamma")) + "\t" + str(opt_params.get("subsample")) + "\t" +
                    str(opt_params.get("reg_lambda")) + "\t" + str(TestR2) + "\t" + str(TestRMSE) + "\t" + str(ValR2) +
                    "\t" + str(ValRMSE) + "\t" + str(TrainR2) + "\t" + str(TrainRMSE) + "\n")
            f.flush()






