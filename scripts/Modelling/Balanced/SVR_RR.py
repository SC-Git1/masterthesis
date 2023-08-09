import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.svm import SVR
import resreg


def objective(trial):
    """Define the objective function"""

    # define the hyperparameter space
    params = {
        'C': trial.suggest_float('C', 10000, 1000000, log = True),
        'epsilon': trial.suggest_float('epsilon', 0.001, 100, log=True),
        'kernel': "rbf",
    }

    # initialize and fit the model for this trial
    optuna_model = SVR(**params)

    optuna_model.fit(X_train, y_train.squeeze())

    # Make predictions
    y_pred = optuna_model.predict(X_val)

    # Evaluate predictions
    accuracy = mean_squared_error(y_val, y_pred)
    return accuracy


if __name__ == "__main__":

    # import the data
    dfInput = pd.read_csv("All_Input_.tsv", sep="\t", header=0)
    random_state = 8
    dfInput = dfInput.sample(frac=1, random_state=random_state).reset_index()

    # define the predictors and the target
    Xcols = [i for i in dfInput.columns if i.endswith("_mean")]
    dfX = dfInput[Xcols]
    dfY = dfInput["Temp"]
    print(dfY)

    # open the output file
    with open("SVR_Resampling.tsv", mode="a") as f:
        f.write("random_state" + "\t" + "random_state" + "\t" + "max_depth" + "\t" + "learning_rate" + "\t" +
                + "n_estimators" + "\t" + "min_child_weight" + "\t" + "gamma" + "\t" + "subsample" + "\t" + "reg_lambda" + "\n")

        for random_state in range(1, 11):
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
            study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(
                seed=random_state))  # maximise the score during tuning

            study.optimize(objective, n_trials=100)

            # extract the best hyperparameters
            trial = study.best_trial
            opt_params = trial.params

            # define the SVR model with optima hyperparameters and fit
            opt_model = SVR(kernel = "rbf", C = opt_params.get("C"), epsilon = opt_params.get("epsilon"))
            opt_model.fit(X_train, y_train)

            # get R² and RMSE on the training, validation and test set
            TestR2 = r2_score(y_test, opt_model.predict(X_test))
            ValR2 = r2_score(y_val, opt_model.predict(X_val))
            TrainR2 = r2_score(y_train, opt_model.predict(X_train))
            TestRMSE = mean_squared_error(y_test, opt_model.predict(X_test), squared=False)
            ValRMSE = mean_squared_error(y_val, opt_model.predict(X_val), squared=False)
            TrainRMSE = mean_squared_error(y_train, opt_model.predict(X_train), squared=False)


            f.write(str(random_state) + "\t" + str(opt_params.get("max_depth")) + "\t" + str(
                opt_params.get("min_samples_split")) +
                "\t" + str(opt_params.get("C")) + "\t" + str(opt_params.get("epsilon")) +
                "\t" + str(TestR2) + "\t" + str(TestRMSE) + "\t" + str(ValR2) +
                "\t" + str(ValRMSE) + "\t" + str(TrainR2) + "\t" + str(TrainRMSE) + "\n")
            f.flush()





