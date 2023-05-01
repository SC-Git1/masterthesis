import pandas as pd
from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient
import time

def getLineage(taxid):
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
            rank_name[elData.get("taxonomy_nodes")[0].get("taxonomy").get("rank")] = elData.get("taxonomy_nodes")[0]. \
                get("taxonomy").get("organism_name")
    except:
        pass
    return rank_name

if __name__ == "__main__":
    # import data
    df = pd.read_csv("NewGenomesSpecies.tsv", sep = "\t", header = 0)

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    Genomes = df["Genome"]
    ncbiTaxIDs = df["ncbiTaxID"]

    with open("to_extractLineageSpecies.tsv", "w") as f:
        f.write("ncbiTaxID" + "\t" + "Genome" + "\t" + "Superkingdom" + "\t" + "Phylum" + "\t" + "Class" + "\t" +
                "Order" + "\t" + "Family" + "\t" + "Genus" + "\n")
        for i in range(len(ncbiTaxIDs)):
            el = str(ncbiTaxIDs[i])
            rank_name = getLineage(el)

            Superkingdom = rank_name.get("SUPERKINGDOM")
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
            # write to file
            f.write(el + "\t" + Genomes[i] + "\t" + Superkingdom + "\t" + Phylum + "\t" + Class + "\t" + Order + "\t" +
                    Family + "\t" + Genus + "\n")
            f.flush()
