import pandas as pd
import resreg
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Import data
    dfInput = pd.read_csv("All_Input_.tsv", sep="\t", header=0)
    random_state = 8
    dfInput = dfInput.sample(frac=1, random_state=random_state).reset_index()

    # define the predictors and target
    Xcols = [i for i in dfInput.columns if i.endswith("_mean")]
    dfX = dfInput[Xcols]
    dfY = dfInput["Temp"]

    ## create a uniform test set

    bins = [22, 32, 45, 60]

    train_indices, test_indices = resreg.uniform_test_split(dfX, dfY, bins=bins,
                                                            bin_test_size=0.5, verbose=True,
                                                            random_state=random_state)
    X_train, y_train = dfX.iloc[train_indices, :], dfY[train_indices]
    X_test, y_test = dfX.iloc[test_indices, :], dfY[test_indices]

    y_testUnbalanced = dfY

    # plot the uniform test set against the unbalanced data
    sns.histplot(y_test.squeeze(), color = "orangered", label = "Uniform", stat = "density", kde = "True")
    sns.histplot(y_testUnbalanced.squeeze(), color = "navy", label = "Unbalanced", stat = "density", kde = "True")
    plt.xlabel("Temperature [°C]")
    plt.legend()
    plt.show()
