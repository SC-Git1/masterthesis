import pandas as pd

# import data
dfNow = pd.read_csv("df_preprocess1.tsv", sep = "\t", header = 0, dtype = {"ncbiTaxID":str})
CorrectIDs = pd.read_csv("CorrectIDsThermoBase_man.txt", sep = "\t", header = 0, dtype={"ID":str})

# update the NCBI Taxonomy IDs
dfNow["ncbiTaxID"] = CorrectIDs["ID"]
# print(len(dfNow)) # 1234 records
dfNow = dfNow[dfNow["Temp"].notna() & (dfNow["ncbiTaxID"] != "-1")]
# print(len(dfNow)) # there are 1203 with a Taxonomy and a temperature annotation

# write to file
dfNow.to_csv("df_preprocessed.tsv", sep = "\t", index = False)

