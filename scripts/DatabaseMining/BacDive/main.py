import pandas as pd
from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient
import time

def get_lineage_from_taxid(taxid):
    rank_name = {}

    data = taxon_api.taxonomy_metadata(taxons=[taxid])
    list_lineage = data.get("taxonomy_nodes")[0].get("taxonomy").get("lineage")
    # remove the root
    list_lineage.remove(1)
    list_lineage.remove(131567)

    for el in list_lineage:
        # get rank and name
        elData = taxon_api.taxonomy_metadata(taxons=[str(el)])
        rank_name[str(elData.get("taxonomy_nodes")[0].get("taxonomy").get("rank"))] = elData.get("taxonomy_nodes")[0]. \
            get("taxonomy").get("organism_name")
    try:
        for el in list_lineage:
            time.sleep(0.1)
            # get rank and name
            elData = taxon_api.taxonomy_metadata(taxons=[str(el)])
            rank_name[elData.get("taxonomy_nodes")[0].get("taxonomy").get("rank")] = elData.get("taxonomy_nodes")[0].\
                get("taxonomy").get("organism_name")
    except:
        pass
    return rank_name

if __name__ == '__main__':

    dfEntry = pd.read_csv("bacdive_entry_df.txt", delimiter="\t", header = 0)
    # print(len(dfEntry)) -> there are initially 17707 records
    # remove no or inconsistent growth data
    dfEntry = dfEntry[(dfEntry["growth"] != "no") & (dfEntry["growth"] != "inconsistent")]
    # print(len(dfEntry)) -> 17463 records have a temperature annotation of type = optimum, growth, minimum or maximum
    # remove those without temperature annotation
    dfEntry = dfEntry[dfEntry['temperature'].notna()]
    # print(len(dfEntry)) -> 17440 records have a valid, existing temperature annotation
    print(dfEntry.groupby(['type', 'growth']).count())
    dfEntry.drop_duplicates(subset=["BacDiveID","type", "temperature"], inplace= True, ignore_index=True)
    # print(len(dfEntry)) # 13273 records remain after removing duplicates i.e.,
    # points with the same source id, temperature value and temperature annotation type

    ### Next, if optimum temperature annotation is available, keep those and discard other types for that BacDive ID
    #keep all rows of BacDiveIDs with optimum temperature available
    subset = dfEntry.groupby(['BacDiveID']).filter(lambda s: (s['type'] == 'optimum').any())
    # keep only their optimal temperature record(s)
    subset = subset[subset["type"] == "optimum"]
    # get all BacDiveIDs
    allIDs = list(dfEntry['BacDiveID'].unique())
    # get all BacDiveIDs included in subset
    subsetIDs = list(subset["BacDiveID"].unique())
    # find remaining IDs
    remainingIDs = list(set(allIDs).difference(set(subsetIDs)))
    # get all data points of the remaining IDs
    remaining = dfEntry[dfEntry["BacDiveID"].isin(remainingIDs)]
    # concatenate in a new dataframe 'dfNew'
    dfNew = pd.concat([subset, remaining])
    dfNew = dfNew.sort_values(by=['BacDiveID'])
    dfNew.reset_index(inplace=True)
    # print(len(dfNew)) -> there are 9534 remaining records
    # print(len(Taxids.unique())) -> the records represent 4677 unique taxonomy IDs
    Taxids = dfNew["id"]
    Species = dfNew["name"]
    Temps = dfNew["temperature"]
    BacDiveIDs = dfNew["BacDiveID"]
    Types = dfNew["type"]

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    with open("NCBI_Annotated_BacDive2.tsv", "a") as f:
        #f.write("Source_ID" + "\t" + "ncbiTaxID" + "\t" + "Name" + "\t" + "Type" + "\t" + "Temp" +
        #        "\t" + "Superkingdom" + "\t" + "Phylum" + "\t" + "Class" + "\t" + "Order" + "\t" + "Family" + "\t" +
        #        "Genus" + "\n")
        for i in range(4995, len(Taxids)):
            el = str(Taxids[i])
            print(el)

            time.sleep(0.4)
            rank_name = get_lineage_from_taxid(el)
            try:
                print(rank_name)
                Superkingdom = rank_name.get("SUPERKINGDOM")
                if Superkingdom == None:
                    Superkingdom = ""
                Phylum = rank_name.get("PHYLUM")
                if Phylum == None:
                    Phylum = ""
                Class = rank_name.get("CLASS")
                if Class == None:
                    Class = ""
                Order = rank_name.get("ORDER")
                if Order == None:
                    Order = ""
                Family = rank_name.get("FAMILY")
                if Family == None:
                    Family = ""
                Genus = rank_name.get("GENUS")
                if Genus == None:
                    Genus = ""
            except:
                pass
            f.write(
                str(BacDiveIDs[i]) + "\t" + el + "\t" + Species[i] + "\t" + Types[i] + "\t" + str(
                    Temps[i]) + "\t" + Superkingdom + "\t"
                + Phylum + "\t" + Class + "\t" + Order + "\t" + Family + "\t" + Genus + "\n")
            f.flush()

