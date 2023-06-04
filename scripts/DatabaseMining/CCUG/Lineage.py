import pandas as pd
from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient
import time


def get_lineage_from_taxid(taxid):

    rank_name = {}

    data = taxon_api.taxonomy_metadata(taxons=[taxid])
    list_lineage = data.get("taxonomy_nodes")[0].get("taxonomy").get("lineage")

    # remove the root and the node "cellular organisms"
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
    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    # import data
    dfCCUG = pd.read_csv("NCBITaxID_CCUG_man.tsv", delimiter="\t", header=0, index_col=False, encoding='latin1')
    # print(len(dfCCUG[dfCCUG["ncbiTaxID"] == -1]))  # 5 records do not haven an NCBI Taxonomy ID annotation
    dfCCUG = dfCCUG[dfCCUG["ncbiTaxID"] != -1]
    dfCCUG.reset_index(inplace=True)

    # Source_ID	Name	Temp	ncbiTaxID
    Taxids = dfCCUG["ncbiTaxID"]
    Source_IDs = dfCCUG["Source_ID"]
    Names = dfCCUG["Name"]
    Temps = dfCCUG["Temp"]

    #SUPERKINGDOM, PHYLUM, CLASS, ORDER, FAMILY, GENUS
    with open("NCBI_Annotated_CCUG.tsv", "w") as f:
        # header
        f.write("ncbiTaxID" + "\t" + "Source_ID" + "\t" + "Name" + "\t" + "Temp" + "\t" + "Superkingdom" + "\t" +
                "Phylum" + "\t" + "Class" + "\t" + "Order" + "\t" + "Family" + "\t" + "Genus" + "\n")

        for i in range(len(Taxids)):
            el = str(Taxids[i])

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

            # write to file
            f.write(el + "\t" + str(Source_IDs[i]) + "\t" + Names[i] + "\t" + Temps[i] + "\t" + Superkingdom + "\t"
                + Phylum + "\t" + Class + "\t" + Order + "\t" + Family  + "\t" + Genus + "\n")
            f.flush()