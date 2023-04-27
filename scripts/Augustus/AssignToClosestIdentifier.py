import pandas as pd


# import data
dfAccs = pd.read_csv("NCBI_Annotated_EukaryoticGenomes.tsv", sep = "\t", header = 0)
dfAug = pd.read_csv("NCBI_Annotated_AugustusUpdated.tsv", sep = "\t", header = 0)

with open("ClosestIdentifier.tsv", "w") as f:
    # header
    f.write("Genome" + "\t" + "ID" + "\t" + "Identifier" + "\t" + "Level" + "\n")

    for i in range(len(dfAccs["Genome"])):
        Assembly = dfAccs.iloc[i]["Genome"]
        ID = dfAccs.iloc[i]["ID"]
        Genus = dfAccs.iloc[i]["Genus"]
        Family = dfAccs.iloc[i]["Family"]
        Order = dfAccs.iloc[i]["Order"]
        Class = dfAccs.iloc[i]["Class"]
        Phylum = dfAccs.iloc[i]["Phylum"]

        """
        ## The selection of a pre-trained species in Augustus goes as follows:
        With increasing rank (Genus to Phylum), try to find a representative in the species list of Augustus ('dfAug')
        If a representative is available, return its identifier. If multiple species match the condition, take the first 
        occurence. If no match is found, go to the next rank. Repeat up to phylum. If at the end no match was found, 
        then set the identifier to 'generic' and the level to 'root'.
        Note: for accuracy reasons, the (super)kingdom level were left out.
        """

        if Genus == Genus and Genus in list(dfAug["Genus"]):
            Identifier = dfAug[dfAug["Genus"].isin([Genus])].iloc[0]["Identifier"]
            Level = "Genus"

        elif Family == Family and Family in list(dfAug["Family"]):
            Identifier = dfAug[dfAug["Family"].isin([Family])].iloc[0]["Identifier"]
            Level = "Family"

        elif Order == Order and Order in list(dfAug["Order"]):
            Identifier = dfAug[dfAug["Order"].isin([Order])].iloc[0]["Identifier"]
            Level = "Order"

        elif Class == Class and Class in list(dfAug["Class"]):
            Identifier = dfAug[dfAug["Class"].isin([Class])].iloc[0]["Identifier"]
            Level = "Class"

        elif Phylum == Phylum and Phylum in list(dfAug["Phylum"]):
            Identifier = dfAug[dfAug["Phylum"].isin([Phylum])].iloc[0]["Identifier"]
            Level = "Phylum"

        else:
            Identifier = "generic"
            Level = "root"

        f.write(Assembly + "\t" + str(ID) + "\t" + Identifier + "\t" + Level + "\n")
        f.flush()