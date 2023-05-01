import pandas as pd

# import data
df = pd.read_csv("ncbiTaxID_CECT2WithBacDive.tsv", sep = "\t", header = 0, encoding="latin1", dtype={'ncbiTaxID': str})
syns = pd.read_csv("synonyms.tsv", sep = "\t", header = 0, dtype={'ncbiTaxID': str})

for i, row in df.iterrows():
    if row["ncbiTaxID"] == "-1":
        # If name + strain matches, print the index in syns and update the value in df
        if row["Name"] + (" " + row["Strain"] if not pd.isnull(row["Strain"]) else "") in syns["Synonym"]:
            idx = syns[syns['Synonym'] == row["Name"]].index.values
            print(idx)
            df.at[i, 'ncbTaxID'] = syns["ncbiTaxID"][idx]

    if row["ncbiTaxID"] == "-1":
        # If the name matches, print the index in syns and update the value in df
        if row["Name"] in syns["Synonym"]:
            idx = syns[syns['Synonym'] == row["Name"]].index.values
            print(idx)
            df.at[i, 'ncbTaxID'] = syns["ncbiTaxID"][idx]
