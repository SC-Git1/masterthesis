import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pingouin as pg


def bland_altman_plot(data1, data2, Domains):
    data1 = np.asarray(data1)
    data2 = np.asarray(data2)
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2  # Difference between data1 and data2
    md = np.mean(diff)  # Mean of the difference
    sd =  np.std(diff, axis=0) # Standard deviation of the difference
    print(sd)
    print(np.median(np.absolute(diff - np.median(diff))))
    print(md)
    CI_low = md - 1.96 * sd / len(diff)
    CI_high = md + 1.96 * sd / len(diff)


    sns.scatterplot(x= mean, y = diff, s = 10, hue = Domains,
                    palette={"Bacteria":"navy", "Archaea":"crimson", "Eukaryota":"limegreen"})
    plt.legend().remove()
    plt.axhline(md, color='black', linestyle='-')
    plt.axhline(md + 1.96 * sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96 * sd, color='gray', linestyle='--')

    plt.xlabel("Means")
    plt.ylabel("Difference")
    plt.ylim(md - 3.5 * sd, md + 3.5 * sd)
    xOutPlot = np.min(mean) + (np.max(mean) - np.min(mean)) * 1.14
    plt.text(xOutPlot, md - 1.96 * sd, r'1.96 SD:' + "\n" + "%.3f" % CI_low, ha="center", va="center")
    plt.text(xOutPlot, md + 1.96 * sd, r'1.96 SD:' + "\n" + "%.3f" % CI_high, ha="center", va="center" )
    plt.text(xOutPlot, md, r'Mean:' + "\n" + "%.2f" % md, ha="center", va="center")
    plt.subplots_adjust(right=0.85)
    plt.show()


if __name__ == "__main__":
    # import data
    dfUni = pd.read_csv("Uni_.tsv", sep = "\t", header = 0)
    df = pd.read_csv("All_Input_.tsv", sep = "\t", header = 0)
    dfLin = pd.read_csv("All_Input_.tsv", sep = "\t", header = 0)

    # subset of TaxIds present in both the predicted set and Swiss-Prot
    sharedTaxIds = list(set(dfUni["ncbiTaxID"]) & set(df["ncbiTaxID"]))
    df = df[df["ncbiTaxID"].isin(sharedTaxIds)].reset_index().sort_values(by=['ncbiTaxID'])
    dfUni = dfUni[dfUni["ncbiTaxID"].isin(sharedTaxIds)].reset_index().sort_values(by=['ncbiTaxID'])

    # define the
    filter_col = [col for col in df if col.endswith("mean")]

    # create a dataframe with the features for both methods
    dfUni["Rater"] = "UniProt"
    df["Rater"] = "Predicted"

    new_df = pd.concat([dfUni,df])

    print(dfUni["Z1_mean"].mean())

    # choose a descriptor (here: VHSE5_mean as an example) to plot
    for col in filter_col:
        if col == "VHSE5_mean":
            bland_altman_plot(df[col], dfUni[col], dfUni["Domain"])
        # get the ICC values for the descriptor defined as 'col' in the function below
        icc_df = pg.intraclass_corr(data=new_df, targets='ncbiTaxID', raters='Rater', ratings=col)


