import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler


def objective(trial):

    params = {
        'C': trial.suggest_float('C', 0.001, 10000, log = True),
        'epsilon': trial.suggest_float('epsilon', 0.001, 4, log=True),
        'kernel': "rbf",
    }

    # define and train SVR model of this trial
    optuna_model = SVR(**params)

    optuna_model.fit(X_train, y_train)

    # Make predictions
    y_pred = optuna_model.predict(X_val)

    # Evaluate predictions
    accuracy = mean_squared_error(y_val, y_pred)
    return accuracy


if __name__ == "__main__":
    # import the data
    dfInput = pd.read_csv("All_Input_noCCT.tsv", sep="\t", header=0)

    filter_col = [i for i in dfInput.columns if i.endswith("mean")]
    X = dfInput[filter_col]
    y = dfInput["Temp"]

    # scaling is very important in the case of SVR!! - else nothing learned, MSE = ~750
    X = pd.DataFrame(StandardScaler().fit_transform(X))

    y = dfInput["Temp"]

    # open the output file
    with open("SVR_results_noCCT_TPE.tsv", mode="a") as f:
        f.write("random_state" + "\t" + "C" + "\t" + "epsilon" + "\t" + "TestR2" + "\t" + "TestRMSE" + "\t" +
                "ValR2" + "\t" + "ValRMSE" + "\t" + "TrainR2" + "\t" + "TrainRMSE" + "\n")

        for random_state in range(1, 11):
            # split into training, test and validation set
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=random_state)
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.11, random_state=random_state)  # 0.25 x 0.8 = 0.2

            # balance the validation set
            y_valExt = y_val[(y_val > 40) | (y_val < 22)]
            y_mes = y_val[(y_val < 40) & (y_val > 22)]
            minlen = min(len(y_valExt), len(y_mes))
            y_val = pd.concat([y_valExt[0:minlen], y_mes[0:minlen]])
            X_val = X_val.loc[y_val.index]

            # intialize and start the Optuna search
            study = optuna.create_study(direction = "minimize", sampler=optuna.samplers.TPESampler(seed=random_state)) # maximise the score during tuning

            study.optimize(objective, n_trials=100) # run the objective function 100 times: # ,callbacks=[neptune_callback]

            # select the best hyperparameters
            trial = study.best_trial
            opt_params = trial.params

            # train an SVR model on the best hyperparameters
            opt_model = SVR(kernel = "rbf", C = opt_params.get("C"), epsilon = opt_params.get("epsilon"))

            opt_model.fit(X_train, y_train)  # early_stoppng_rounds = 20

            # calculate the R² and RMSE on the training, test and validation set
            TestR2 = r2_score(y_test, opt_model.predict(X_test))
            ValR2 = r2_score(y_val, opt_model.predict(X_val))
            TrainR2 = r2_score(y_train, opt_model.predict(X_train))
            TestRMSE = mean_squared_error(y_test, opt_model.predict(X_test), squared=False)
            ValRMSE = mean_squared_error(y_val, opt_model.predict(X_val), squared = False)
            TrainRMSE = mean_squared_error(y_train, opt_model.predict(X_train), squared=False)


            # write to output file
            f.write(str(random_state) + "\t" + str(opt_params.get("C")) + "\t" + str(opt_params.get("epsilon")) + "\t" +
                   str(TestR2) + "\t" + str(TestRMSE) + "\t" + str(ValR2) + "\t" + str(ValRMSE) + "\t" + str(TrainR2) +
                   "\t" + str(TrainRMSE) + "\n")
            f.flush()

