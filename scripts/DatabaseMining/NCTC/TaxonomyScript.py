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

if __name__ == "__main__":
    # import data
    dfNCTC = pd.read_csv("ncbiTaxID_NCTC_man.tsv", delimiter="\t", header=0, dtype={"ncbiTaxID":str})
    # print(len(dfNCTC)) # 3511
    # remove all records without an NCBI Taxonomy annotation
    dfNCTC = dfNCTC[dfNCTC["ncbiTaxID"] != "-1"]
    dfNCTC.reset_index(inplace=True)
    # print(len(dfNCTC)) # 3402 remaining records

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    Names = dfNCTC["Species"]
    Taxids = dfNCTC["ncbiTaxID"]
    SourceIDs = dfNCTC["Source_ID"]
    Strains = dfNCTC["Strain"]
    Temps = dfNCTC["Temp"]

    #SUPERKINGDOM, PHYLUM, CLASS, ORDER, FAMILY, GENUS

    with open("NCBI_Annotated_NCTC5.tsv", "w") as f:
        f.write("ncbiTaxID" + "\t" + "Source_ID" + "\t" + "Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "Superkingdom" + "\t" +
            "Phylum" + "\t" + "Class" + "\t" + "Order" + "\t" + "Family" + "\t" + "Genus" + "\n")
        for i in range(len(Taxids)):
            el = str(Taxids[i])
            rank_name = get_lineage_from_taxid(el)
            
            try:
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

            f.write(el + "\t" + str(SourceIDs[i]) + "\t" + Names[i] + "\t" + (str(Strains[i]).replace(u"\x85","a") if Strains[i] else "") +
                "\t" + str(Temps[i]) + "\t" + Superkingdom + "\t" + Phylum + "\t" + Class + "\t" + Order + "\t" +
                Family + "\t" + Genus + "\n")
            f.flush()
