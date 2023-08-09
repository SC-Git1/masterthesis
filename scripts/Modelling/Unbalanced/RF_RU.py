import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor


def objective(trial):

    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 1000),
        'max_depth': trial.suggest_int('max_depth', 1, 10),
        'min_samples_split': trial.suggest_float('min_samples_split', 1e-8, 1, log = True),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 2, 60),
        'ccp_alpha': trial.suggest_float('ccp_alpha', 0.1, 100, log=True), # previous it was 0.87 against 0.79 if 1e-3
        'random_state': 5,
        'n_jobs': -1
    }

    optuna_model = RandomForestRegressor(**params)

    optuna_model.fit(X_train, y_train)

    # Make predictions
    y_pred = optuna_model.predict(X_val)

    # Evaluate predictions
    accuracy = mean_squared_error(y_val, y_pred)
    return accuracy


if __name__ == "__main__":
    # import data
    dfInput = pd.read_csv("All_Input_.tsv", sep ="\t", header = 0)
    dfInput = dfInput.dropna().reset_index(drop = True)

    # select descriptor, work with means
    filter_col = [i for i in dfInput.columns if i.endswith("mean")]
    X = dfInput[filter_col]
    y = dfInput["Temp"]

    # open output file
    with open("RF_results_TPE.tsv", mode="a") as f:
        # write header
        f.write("random_state" + "\t" + "n_estimators" + "\t" + "max_depth" + "\t" + "min_samples_split" +
                "\t" + "min_samples_leaf" + "\t" + "ccp_alpha" + "\t" + "TestR2" + "\t" +
                "TestRMSE" + "\t" + "ValR2" + "\t" + "ValRMSE" + "\t" + "TrainR2" + "\t" + "TrainRMSE" + "\n")

        # for ten iterations
        for random_state in range(1,11):

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=random_state)
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.11,
                                                              random_state=random_state)  # 0.25 x 0.8 = 0.2

            ## balanced validation set
            y_valExt = y_val[(y_val > 40) | (y_val < 22)]
            y_mes = y_val[(y_val < 40) & (y_val > 22)]
            minlen = min(len(y_valExt), len(y_mes))
            print(minlen)
            y_val = pd.concat([y_valExt[0:minlen], y_mes[0:minlen]])
            X_val = X_val.loc[y_val.index]

            # set up Optuna
            study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=random_state)) # maximise the score during tuning
            study.optimize(objective, n_trials=100)

            # print the hyperparameters  etc.
            trial = study.best_trial

            opt_params = trial.params

            # train best model on training data
            opt_model = RandomForestRegressor(max_depth = opt_params.get("max_depth"), min_samples_split  = opt_params.get("min_samples_split"),
                                     n_estimators = opt_params.get("n_estimators"), min_samples_leaf = opt_params.get("min_samples_leaf"),
                                     ccp_alpha=opt_params.get('ccp_alpha'))

            opt_model.fit(X_train, y_train)

            # get test, validation and train R² and RMSE
            TestR2 = r2_score(y_test, opt_model.predict(X_test))
            ValR2 = r2_score(y_val, opt_model.predict(X_val))
            TrainR2 = r2_score(y_train, opt_model.predict(X_train))
            TestRMSE = mean_squared_error(y_test, opt_model.predict(X_test), squared=False)
            ValRMSE = mean_squared_error(y_val, opt_model.predict(X_val), squared=False)
            TrainRMSE = mean_squared_error(y_train, opt_model.predict(X_train), squared=False)

            # write to file
            f.write(str(random_state) + "\t" + str(opt_params.get("n_estimators")) + "\t" + str(opt_params.get("max_depth")) +
                    "\t" + str(opt_params.get("min_samples_split")) + "\t" + str(opt_params.get("min_samples_leaf")) +
                    "\t" + str(opt_params.get("ccp_alpha")) + "\t" + str(TestR2) + "\t" + str(TestRMSE) + "\t" + str(ValR2) +
                    "\t" + str(ValRMSE) + "\t" + str(TrainR2) + "\t" + str(TrainRMSE) + "\n")
            f.flush()





