import pandas as pd
import re
import numpy as np

# import data
df_NCTC = pd.read_csv("NCTC_extracted3.txt",delimiter = "\t", encoding_errors = "replace", index_col=False)

# Ensure the first part of the names are uppercase because sometimes missing
df_NCTC['Species'] = df_NCTC['Species'].str.capitalize()
# print(len(df_NCTC[(df_NCTC['Cond_solid'] != "NA") & (df_NCTC['Cond_liquid'] == "NA")])) # 0
# print(len(df_NCTC[(df_NCTC['Cond_solid'] == "NA") & (df_NCTC['Cond_liquid'] != "NA")])) # 0

df_NCTC = df_NCTC[(df_NCTC['Cond_solid'] != "NA") & (df_NCTC['Cond_liquid'] != "NA")]
# print(len(df_NCTC)) # 5724
new_col_solidT = []
new_col_liquidT = []
for i in df_NCTC.index:
    # get temperature for growth on solid media
    try:
        new_col_solidT.append(re.search(",([0-9]+),",str(df_NCTC.at[i,'Cond_solid'])).group(1))
    except AttributeError:
        new_col_solidT.append("NA")

    # get temperature for growth on liquid media
    try:
        new_col_liquidT.append(re.search(",([0-9]+),",str(df_NCTC.at[i,'Cond_liquid'])).group(1))
    except AttributeError:
        new_col_liquidT.append("NA")

df_NCTC['solidT'] = new_col_solidT
df_NCTC['liquidT'] = new_col_liquidT
# print(sum(df_NCTC['liquidT'] == "NA")) # 2235
# print(sum(df_NCTC['solidT'] == "NA")) # 3526
# print(len(df_NCTC[(df_NCTC['liquidT'] == "NA") & (df_NCTC['solidT'] == "NA")])) # 2213

# df_NCTC = df_NCTC[(df_NCTC['solidT'] != "NA") & (df_NCTC['liquidT'] != "NA")]
# print(len(df_NCTC)) # 2176
# print(sum(df_NCTC['solidT'] == df_NCTC['liquidT'])) # 2176
# -> so, if both are present, than there values are the same

# Create a new column 'Temp' that is equal to the solidT value, unless no value is present, than use the liquidT value
df_NCTC["Temp"] = np.where(df_NCTC["solidT"] == "NA", df_NCTC["liquidT"], df_NCTC["solidT"])
print(sum(df_NCTC["Temp"] != "NA")) # 3511

# export data
df_NCTC.rename(columns = {"NCTC_number":"Source_ID"}, inplace=True)
df_NCTC = df_NCTC[df_NCTC["Temp"] != "NA"]
df_NCTC[['Species', "Strain",'Source_ID','Temp']].to_csv('NCTC_extracted_withTemp.tsv', sep = '\t', index= False)
