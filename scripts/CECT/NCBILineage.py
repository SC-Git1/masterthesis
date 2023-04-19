import pandas as pd
from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient
import time

def get_lineage_from_taxid(taxid):
    """
    Returns a list of lists
    """
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
    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)
    df = pd.read_csv("ncbiTaxID_CECT2_man.tsv", delimiter="\t", header=0, index_col=False, dtype={"ncbiTaxID":str})
    # print(len(df)) # 7991
    df = df[df["ncbiTaxID"] != "-1"]
    df.reset_index(inplace=True)
    print(len(df)) # 7600
    Names = df['Name']
    Strains = df["Strain"]
    Temps = df['Temp']
    SourceIDs = df['Source_ID']
    IDs = df["ncbiTaxID"]

    with open("NCBI_Annotated_CECT2.tsv", "w") as f:
        f.write("ncbiTaxID" + "\t" + "Source_ID" + "\t" + "Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "Superkingdom" + "\t" +
                "Phylum" + "\t" + "Class" + "\t" + "Order" + "\t" + "Family" + "\t" + "Genus" + "\n")
        for i in range(len(IDs)):
            el = str(IDs[i])
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
            f.write(el + "\t" + str(SourceIDs[i]) + "\t" + Names[i].replace(u'\ufffd',"?") + "\t" + (str(Strains[i]) if Strains[i] else "").replace(u'\ufffd',"?") + "\t" +
                str(Temps[i]) + "\t" + Superkingdom + "\t" + Phylum + "\t" + Class + "\t" + Order + "\t" + Family + "\t" +
                Genus + "\n")
            f.flush()