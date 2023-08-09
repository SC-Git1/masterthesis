import pandas as pd


# import data
dfTotal = pd.read_csv("Total.tsv", sep = "\t", header = 0)

# remove NCTC records
dfTotal = dfTotal[dfTotal["Source"] != "NCTC"]
print(len(dfTotal)) # 34781


# find the number of different IDs that are present in the entire dataset
dfTotal["ncbiTaxID"] = dfTotal["ncbiTaxID"].astype(str)
print(len(dfTotal))
print(len(dfTotal["ncbiTaxID"].drop_duplicates())) # 34781 -> 17379


# if for an NCBI Taxonomy ID a record of type "optimum" is present, remove those of type "growth" for that ID
# get all optimum records
dfOpt = dfTotal[dfTotal["Type"] == "optimum"]
# get all IDs with at least one record of the type "optimum"
AllOptIDs = list(dfOpt["ncbiTaxID"])
# get all records of IDs without an "optimum" record
dfGrowth = dfTotal[~dfTotal["ncbiTaxID"].isin(AllOptIDs)]
# concatenate
dfTotal2 = pd.concat([dfOpt, dfGrowth])
print(len(dfTotal2)) # 28550

dfTotal2 = dfTotal2[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order', 'Family', 'Genus', 'Source', 'Source_ID']]
dfTotal2.to_csv("CleanedData.tsv", sep = "\t", index=False)

