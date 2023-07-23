import pandas as pd


"""
The included columns in the final database are: 
1) ncbiTaxID, 2) Name, 3) Strain, 4) Temp, 5) Type: either "optimum" or "growth", 6) Superkingdom,
7) Phylum 8) Class, 9) Order, 10) Family, 11) Genus, 12) Source: name of the database. Possible values are
"MediaDB", "BacDive", "aciDB", "ThermoBase", "CCUG", "CECT", "NIES", "NCTC", or "Lyubetsky et al., 2020", 
13) Source_ID: record Id in the database or else Source + i with i = 1, 2,... in the order of appearance.
"""

### MediaDB
dfMediaDB = pd.read_csv("NCBI_Annotated_MediaDB2.tsv", header = 0, sep = "\t")
dfMediaDB["Source"] = "MediaDB"
# set default Source_IDs: MediaDB1, MediaDB2, etc.
dfMediaDB["Source_ID"] = ["MediaDB" + str(x) for x in range(len(dfMediaDB))]
dfMediaDB["Type"] = "growth"
# order the columns
dfMediaDB = dfMediaDB[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order',
                       'Family', 'Genus', 'Source', 'Source_ID']]
# result: 649 records assigned to 69 unique NCBI TaxIds


### BacDive
dfBacDive = pd.read_csv("NCBI_Annotated_BacDive_Corr.tsv", header = 0, sep = "\t")
dfBacDive["Source"] = "BacDive"
dfBacDive["Strain"] = ""
# If a temperature interval is given, calculate the mean value
dfBacDive.loc[dfBacDive['Temp'].astype(str).str.contains("-*[0-9]+-"), 'Temp1'] = \
    dfBacDive["Temp"].str.findall("(-*[0-9]+)-(-*[0-9]+)").str[0].str[0]
dfBacDive.loc[dfBacDive['Temp'].astype(str).str.contains("-*[0-9]+-"), 'Temp2'] = \
    dfBacDive["Temp"].str.findall("(-*[0-9]+)-(-*[0-9]+)").str[0].str[1]
dfBacDive.loc[dfBacDive['Temp'].astype(str).str.contains("-*[0-9]+-"), 'Temp'] = (pd.to_numeric(dfBacDive["Temp2"]) +
                                                                      pd.to_numeric(dfBacDive["Temp1"]))/2
# order the columns
dfBacDive = dfBacDive[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order',
                       'Family', 'Genus', 'Source', 'Source_ID']]
# result: 9543 records assigned to 4677 unique NCBI TaxIds


### aciDB
dfaciDB = pd.read_csv("NCBI_Annotated_aciDB3.tsv", header = 0, sep = "\t", index_col=False)
# set default Source_IDs: aciDB1, aciDB2, etc.
dfaciDB["Source_ID"] = ["aciDB" + str(x) for x in range(len(dfaciDB))]
dfaciDB["Type"] = "optimum"
dfaciDB["Source"] = "aciDB"
# oder the columns
dfaciDB = dfaciDB[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order',
                   'Family', 'Genus', 'Source', 'Source_ID']]
# result: 412 records assigned to 316 unique NCBI TaxIds


### ThermoBase
dfThermoBase = pd.read_csv("NCBI_Annotated_ThermoBase2.tsv", header = 0, sep = "\t", encoding="UTF-8")
dfThermoBase["Source"] = "ThermoBase"
# set default Source_IDs: ThermoBase1, ThermoBase2, etc.
dfThermoBase["Source_ID"] = ["ThermoBase" + str(x) for x in range(len(dfThermoBase))]
dfThermoBase["Type"] = "optimum"
# order the columns
dfThermoBase = dfThermoBase[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order',
                             'Family', 'Genus', 'Source', 'Source_ID']]
# result: 1203 records assigned to 1176 unique NCBI TaxIds


### CCUG
dfCCUG = pd.read_csv("NCBI_Annotated_CCUG.tsv", header = 0, sep = "\t")
dfCCUG["Source"] = "CCUG"
dfCCUG["Type"] = "growth"
dfCCUG["Strain"] =  ""
# If a temperature interval is given, calculate the mean value
dfCCUG.loc[dfCCUG['Temp'].astype(str).str.contains("-*[0-9]+-", regex = True), 'Temp1'] = \
    dfCCUG["Temp"].str.findall("(-*[0-9]+)-(-*[0-9]+)").str[0].str[0]
dfCCUG.loc[dfCCUG['Temp'].astype(str).str.contains("-*[0-9]+-", regex = True), 'Temp2'] = \
    dfCCUG["Temp"].str.findall("(-*[0-9]+)-(-*[0-9]+)").str[0].str[1]
dfCCUG.loc[dfCCUG['Temp'].astype(str).str.contains("-*[0-9]+-", regex = True), 'Temp'] = (pd.to_numeric(dfCCUG["Temp2"]) +
                                                                    pd.to_numeric(dfCCUG["Temp1"]))/2
# order the columns
dfCCUG = dfCCUG[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order',
                 'Family', 'Genus', 'Source', 'Source_ID']]
# result: 2949 records assigned to 2850 unique NCBI TaxIds


### CECT
dfCECT = pd.read_csv("NCBI_Annotated_CECT2.tsv", header=0, sep = "\t", encoding = "unicode_escape")
dfCECT["Source"] = "CECT"
dfCECT["Type"] = "growth"
# order the columns
dfCECT = dfCECT[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order',
                 'Family', 'Genus', 'Source', 'Source_ID']]
# result: 7611 records assigned to 3221 unique NCBI TaxIds


### NIES
dfNIES = pd.read_csv("NCBI_Annotated_NIES.tsv", sep = "\t", header = 0)
dfNIES["Source"] = "NIES"
dfNIES["Type"] = "growth"
dfNIES["Strain"] = dfNIES["Source_ID"]
# order the columns
dfNIES = dfNIES[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order', 'Family',
                 'Genus', 'Source', 'Source_ID']]
# result: 2842 records assigned to 1194 unique NCBI TaxIds


### NCTC
dfNCTC = pd.read_csv("NCBI_Annotated_NCTC5.tsv", header = 0, sep = "\t")
dfNCTC["Source"] = "NCTC"
dfNCTC["Type"] = "growth"
# order the columns
dfNCTC = dfNCTC[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order',
                 'Family', 'Genus', 'Source', 'Source_ID']]
# result: 3402 records assigned to 836 unique NCBI TaxIds


### Lyubetsky et al., 2020
dfLyubetsky2020 = pd.read_csv("NCBI_Annotated_Lyubetsky2020.tsv", header = 0, sep = "\t")
# set default Source_IDs: Lyu1, Lyu2, etc.
dfLyubetsky2020["Source_ID"] = ["Lyu" + str(x) for x in range(len(dfLyubetsky2020))]
dfLyubetsky2020["Type"] = "optimum"
dfLyubetsky2020["Source"] = "Lyubetsky et al., 2020"
# order the columns
dfLyubesky2020 = dfLyubetsky2020[['ncbiTaxID','Name','Strain','Temp','Type','Superkingdom','Phylum','Class','Order',
                                  'Family', 'Genus', 'Source', 'Source_ID']]
# result: 933 records assigned to 914 unique NCBI TaxIds


### TEMPURA
dfTempura = pd.read_csv("NCBI_Annotated_Tempura4.tsv", header = 0, sep = "\t")
dfTempura["Source"] = "Tempura"
# set default Source_IDs: Tempura1, Tempura2, etc.
dfTempura["Source_ID"] = ["Tempura" + str(x) for x in range(len(dfTempura))]
dfTempura["Type"] = "optimum"
# order the columns
dfTempura = dfTempura[['ncbiTaxID', 'Name', 'Strain', 'Temp', 'Type', 'Superkingdom', 'Phylum', 'Class','Order',
                       'Family', 'Genus', 'Source', 'Source_ID']]
# print(len(dfTempura)) #  of which  unique
# result: 8639 records assigned to 8618 unique NCBI TaxIds


dfTotal = pd.concat([dfMediaDB, dfBacDive, dfNCTC, dfThermoBase, dfCCUG, dfLyubetsky2020, dfTempura, dfNIES, dfaciDB,
                     dfCECT])
# write to file
dfTotal.to_csv("Total.tsv", sep = "\t", index = False)

"""



# extra checkpoint




# Now, assess the databases. Come back to clean it up further :)

# "Clean" the data and store it in CleanedData.tsv -> annother script: annotation + one for the handling and all statistics
# on the databases
# in the cleaned version, also remove the NCTC records
# -> CleanWithoutNCTC.tsv

### note: redo analysis in R to correct for the one misannotated record in TEMPURA (but same phylum so not an effect on the
# Phylum tree, however it does have an impact on the absolute counts)
"""