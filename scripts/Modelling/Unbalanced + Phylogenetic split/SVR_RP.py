import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.svm import SVR
from sklearn.cluster import AgglomerativeClustering
from phylodm import PhyloDM
import dendropy
from itertools import groupby


def objective(trial):

    # define the hyperparameter space
    params = {
        'C': trial.suggest_float('C', 0.001, 10000, log = True),
        'epsilon': trial.suggest_float('epsilon', 0.001, 4, log=True),
        'kernel': "rbf",
    }

    # initialize the model for the trial
    optuna_model = SVR(**params)

    # fit
    optuna_model.fit(X_train, y_train)

    # Make predictions
    y_pred = optuna_model.predict(X_val)

    # Evaluate predictions
    accuracy = mean_squared_error(y_val, y_pred)
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

            # build the SVR model with the best hyperparameters
            opt_model = SVR(kernel = "rbf", C = opt_params.get("C"), epsilon = opt_params.get("epsilon"))

            opt_model.fit(X_train, y_train)  # early_stoppng_rounds = 20

            # calculate R² and RMSE on the training, test and validation set
            TestR2 = r2_score(y_test, opt_model.predict(X_test))
            ValR2 = r2_score(y_val, opt_model.predict(X_val))
            TrainR2 = r2_score(y_train, opt_model.predict(X_train))
            TestRMSE = mean_squared_error(y_test, opt_model.predict(X_test), squared=False)
            ValRMSE = mean_squared_error(y_val, opt_model.predict(X_val), squared = False)
            TrainRMSE = mean_squared_error(y_train, opt_model.predict(X_train), squared=False)

            # write to the output file
            f.write(str(random_state) + "\t" + str(opt_params.get("C")) + "\t" + str(opt_params.get("epsilon")) + "\t" +
                   str(TestR2) + "\t" + str(TestRMSE) + "\t" + str(ValR2) + "\t" + str(ValRMSE) + "\t" + str(TrainR2) +
                   "\t" + str(TrainRMSE) + "\n")

            f.flush()
