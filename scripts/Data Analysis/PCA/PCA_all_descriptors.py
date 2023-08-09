import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable



# Function to plot the biplot


if __name__ == "__main__":

    # import data
    df = pd.read_csv("All_Input.tsv", sep = "\t", header = 0)
    df = df.sample(frac=1, random_state=1)
    print(len(df))
    # select all columns containing the mean of an AA descriptor
    filter_col = [col for col in df if col.endswith("mean")]
    X = df[filter_col]

    # scale and decompose using PCA
    Xs = pd.DataFrame(StandardScaler().fit_transform(X), columns = filter_col)

    PCA = PCA(n_components=57, svd_solver = "full")
    components = PCA.fit_transform(Xs)
    dfcomponents = pd.DataFrame(components)
    print(PCA.explained_variance_ratio_)
    dfTempcomp = dfcomponents
    dfTempcomp["Temp"] = df["Temp"]
    print(dfTempcomp.corr())

    # Import the lineage information
    dfL = pd.read_csv("CleanedData.tsv", header = 0, sep = "\t")
    dfL = dfL[['ncbiTaxID', 'Superkingdom', 'Phylum','Class', 'Order', 'Family', 'Genus', "Source"]]
    # merge to AA descriptors information
    dfL = dfL.drop_duplicates("ncbiTaxID").reset_index()
    df = df.merge(dfL, on = "ncbiTaxID", how = "left")

    # PCA plot
    with sns.axes_style("whitegrid"):
        # set up everything for the colorbar
        norm = plt.Normalize(df['Temp'].min(), df['Temp'].max())
        cmap = LinearSegmentedColormap.from_list("", ["blue", "lightgreen", "orangered", "darkred"])
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        ax = sns.scatterplot(x=dfcomponents.iloc[:, 1], y=dfcomponents.iloc[:, 3], hue=df["Temp"], palette=cmap, s=10,
                             edgecolor="darkgrey")
        ax.set_aspect('equal', 'box')
        ax.get_legend().remove()
        plt.title("PCA of all AA descriptors with temperature")
        plt.title("PCA of all AA descriptors with domain")
        EVR1 = PCA.explained_variance_ratio_[0]
        EVR2 = PCA.explained_variance_ratio_[3]
        plt.xlabel("PC2 (" + str(round(EVR1*100, 2)) + " %)")
        plt.ylabel("PC4 (" + str(round(EVR2*100, 2)) + " %)")

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="2%", pad=0.05)
        ax.figure.colorbar(sm, cax=cax)
        plt.show()


    # plot per superkingdom
    with sns.axes_style("whitegrid"):
        # set up everything for the colorbar
        sns.scatterplot(x=dfcomponents.iloc[:, 0], y=dfcomponents.iloc[:, 3], hue=df["Superkingdom"], s=10,
                        palette = ["navy", "crimson", "limegreen"], edgecolor="white")
        ax = plt.gca()
        plt.xlabel("PC1 (" + str(round(EVR1 * 100, 2)) + " %)")
        plt.ylabel("PC2 (" + str(round(EVR2 * 100, 2)) + " %)")
        ax.set_aspect('equal', adjustable='box')
        plt.show()




    # Eukaryan phyla
    dfEuk = df.copy(deep = True)
    dfEuk.loc[dfEuk["Superkingdom"] != "Eukaryota", "Phylum"] = "Unknown"

    with sns.axes_style("whitegrid"):
        # set up everything for the colorbar
        sns.scatterplot(x=dfcomponents.iloc[dfEuk[dfEuk["Superkingdom"] == "Eukaryota"].index, 0],
                        y=dfcomponents.iloc[dfEuk[dfEuk["Superkingdom"] == "Eukaryota"].index, 1], hue=dfEuk["Phylum"],
                        s=20, edgecolor="b", palette= ["silver", "blue", "red", "yellow", "limegreen",
                                "orange", "hotpink", "black", "blueviolet", "lawngreen", "deepskyblue"], style =
                                dfEuk["Phylum"], markers = ['o', 'v', '^', 'P', 's', 'p', '*', 'h','D', 'd', 'X', "x"])
        ax = plt.gca()
        ax.set_aspect('equal')#, adjustable='box')
        plt.title("Phylum distribution in the PCA plot of the Eukaryota")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.xlabel("PC1 (" + str(round(EVR1 * 100, 2)) + " %)")
        plt.ylabel("PC2 (" + str(round(EVR2 * 100, 2)) + " %)")
        plt.tight_layout()
        plt.show()



    # Archaea order
    dfArch = df.copy(deep = True)
    dfArch.loc[dfArch["Superkingdom"] != "Archaea", "Class"] = "Unknown"
    #dfArch.loc[dfArch["Phylum"] != "Euryarchaeota", "Order"] = "other phyla"
    print(set(dfArch["Phylum"]))
    with sns.axes_style("whitegrid"):
        # set up everything for the colorbar
        sns.scatterplot(x=dfcomponents.iloc[dfArch[dfArch["Superkingdom"] == "Archaea"].index, 0],
                        y=dfcomponents.iloc[dfArch[dfArch["Superkingdom"] == "Archaea"].index, 1], hue=dfArch["Class"],
                        s=40, palette= ["wheat", "blue", "black", "red", "limegreen",
                                "orange", "hotpink", "yellow", "blueviolet", "lawngreen", "deepskyblue",
                                                       "coral", "darkgrey", "brown"], style =
                                dfArch["Class"], markers = [',', 'v', '^', 'P', 's', 'p', '*', 'h','D', 'd', 'X', 'H',
                                                            "<", ">"], edgecolor = "darkgrey")
        ax = plt.gca()
        ax.set_aspect('equal')#, adjustable='box')
        plt.title("Phylum distribution in the PCA plot of the Archaea")
        plt.xlabel("PC1 (" + str(round(EVR1 * 100, 2)) + " %)")
        plt.ylabel("PC2 (" + str(round(EVR2 * 100, 2)) + " %)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.show()

        # Bacterial phyla
        dfBact = df.copy(deep=True)
        dfBact.loc[dfBact["Superkingdom"] != "Bacteria", "Phylum"] = "Unknown"
        print(dfBact.groupby("Phylum").count())

        tab20c = plt.cm.get_cmap('tab20c')
        tab20b = plt.cm.get_cmap('tab20b')


        with sns.axes_style("whitegrid"):
            sns.scatterplot(x=dfcomponents.iloc[dfBact[dfBact["Superkingdom"] == "Bacteria"].index, 0],
                            y=dfcomponents.iloc[dfBact[dfBact["Superkingdom"] == "Bacteria"].index, 1],
                            hue=dfBact["Phylum"], s=30, palette='tab20', style = dfBact["Phylum"],
                            markers=[',', '.', 'o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H',
                                                       'D', 'd', 'P', 'X'], edgecolor = "navy")

            ax = plt.gca()
            # plt.colorbar(plt.gcf(), ticks=np.arange(len(dfBact["Phylum"].unique())))
            ax.set_aspect('equal')  # , adjustable='box')
            plt.title("Phylum distribution in the PCA plot of the Bacteria")
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, prop={"size": 8})
            plt.xlabel("PC1 (" + str(round(EVR1 * 100, 2)) + " %)")
            plt.ylabel("PC2 (" + str(round(EVR2 * 100, 2)) + " %)")
            plt.tight_layout()
            plt.show()
