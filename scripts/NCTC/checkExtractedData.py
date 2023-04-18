import  pandas as pd

# import data
df = pd.read_csv("species_avail_in_NCTC_04032023_alphabetical_listing.txt", delimiter ="\t", header = 0, index_col=False)
df.rename(columns = {'Current Name':'Species'}, inplace=True)
# make the species names consistent
df['Species'] = df['Species'].str.capitalize()

# store the number of records per species in a new dataframe df_occ
df_occ = df.groupby(['Species']).aggregate('sum')
df_occ.reset_index(inplace=True)
print(df_occ)

# import record data
df_NCTC = pd.read_csv("NCTC_extracted3.txt",delimiter = "\t", encoding_errors = "replace", index_col=False)
# make the species names consistent
df_NCTC['Species'] = df_NCTC['Species'].str.capitalize()
# print(len(df_NCTC)) ->  there are 5724 retrieved records

# count how many times each Species name appears in the retrieved records
occurences2 = df_NCTC.groupby(['Species']).size()
df_NCTC_occ = occurences2.to_frame()
df_NCTC_occ.index.name = 'Species'
df_NCTC_occ.reset_index(inplace=True)
df_NCTC_occ.columns = ['Species','Found']

# merge to investigate the difference in counts
outer_merged = pd.merge(df_occ, df_NCTC_occ, how="outer", on=["Species"])
outer_merged_clean = outer_merged[outer_merged['Found'] != outer_merged['Number of Results']]
outer_merged_clean.to_csv('CountDifferences.tsv', sep="\t")
print(outer_merged_clean["Found"])

"""
Result:
25 extra names are found in the retrieved data
1 is missing: Smi tp nctc set (17 strains) - NCTC 13121601
However, this record covers 17 strains and has no information on growth conditions -> OK
"""