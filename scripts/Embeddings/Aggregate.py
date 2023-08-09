import pandas as pd


#### Example for Ribosomal

# import data
df = pd.read_csv("Ribosomal_all.txt", sep = "\t", header = None)
df.columns = ["Genome", "#Protein"] + ["UP" + str(i) for i in range (1,1902)]
df = df.drop("UP1901", axis = 1)

# Map the assembly accession to the ncbiTaxID and then to the OGT annotation
dfGenome = pd.read_csv("UniqueCorr.tsv", sep = "\t", header = 0)[["Genome", "ncbiTaxID"]].drop_duplicates("Genome")
df = df.merge(dfGenome, on = "Genome", how = "left")
df = df.drop("Genome", axis = 1)

dfTemp = pd.read_csv("All_Input_.tsv", sep = "\t", header = 0)[["ncbiTaxID","Temp"]]
df = df.merge(dfTemp, on = "ncbiTaxID", how = "left")

# remove NaN
df = df[df["Temp"].notna()]

# collapse to the TaxId
df = df.groupby("ncbiTaxID").mean() # 624

# write to new file
df.to_csv("Mean_Ribosomal.tsv", sep = "\t")