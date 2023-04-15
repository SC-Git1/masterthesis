import pandas as pd
import re


# import the data
dfCond = pd.read_csv("CCUG_info2.txt",delimiter="\t", header=0,index_col=False, encoding="utf-16")

# remove records without information about their growth condition
dfCond = dfCond[dfCond['cond'].notna()]
# print(len(dfCond)) -> there are 3045 remaining records

## extract the temperatures
listT = []
for i in dfCond.index:
    try:
        Temp = re.search(r"([\-0-9()]+)°",dfCond.at[i,'cond']).group(1).replace("(","").replace(")","")

        # if a range of three temperatures is given, only keep the two boundary values
        # e.g. for 45377T: 28-37-(42)°C -> 28-42
        if re.match("[0-9]+-[0-9]+-[0-9]+", Temp):
            Temp = Temp.split("-")[0] + "-" + Temp.split("-")[2]

        # Fix error in record 4311T: 37(30-42)°C, missing "-" in front of (
        elif dfCond.at[i,'CCUG Number'] == "4311T":
            Temp = "30-42"

        listT.append(Temp)

    # if no match found, the temperature annotation is missing the ° symbol, but contains C to denote degrees Celsius
    except AttributeError:
        try:
            Temp = re.search(r"([\-0-9()]+)C", dfCond.at[i, 'cond']).group(1).replace("(","").replace(")","")
            listT.append(Temp)
        except AttributeError:
            # else, the temperature annotation is not present in an unambiguously interpretable format
            # e.g. "room temperature"
            listT.append("NA")

dfCond['Temp'] = listT
dfCond = dfCond[(dfCond['Temp'] != "NA") & (dfCond['Temp'] != "")]
# print(dfCond.shape) -> there are 2954 records with temperature annotation
dfCond.to_csv("Annotated_CCUG2.tsv", sep = "\t", index = False)

# merge to add the species names
df_records = pd.read_csv("Records.tsv",delimiter="\t", header=0,index_col=False)
merged = dfCond.merge(df_records, how = "left", on = "CCUG Number")
merged.filter(['CCUG Number','Strain','Temp']).to_csv("AnnotatedWithSpecies_CCUG2.tsv", sep = "\t", index = False)