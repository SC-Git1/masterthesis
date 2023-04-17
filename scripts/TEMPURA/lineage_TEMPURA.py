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
    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    dfTempura = pd.read_csv("200617_TEMPURA.tsv", sep ="\t", header=0)
    # rename columns
    dfTempura.rename(columns = {"taxonomy_id":"ncbiTaxID", "genus_and_species": "Name", "Topt_ave":"Temp",
                                "assembly_or_accession":"Genome", "strain":"Strain"}, inplace = True)

    IDs = dfTempura["ncbiTaxID"]
    Names = dfTempura['Name']
    Strains = dfTempura["Strain"]
    Temps = dfTempura['Temp']
    Genomes = dfTempura['Genome']

    with open("NCBI_Annotated_Tempura.tsv", "w") as f:
        f.write("ncbiTaxID" + "\t" + "Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "Superkingdom" + "\t" +
                "Phylum" + "\t" + "Class" + "\t" + "Order" + "\t" + "Family" + "\t" + "Genus" + "\t" + "Genome" + "\n")
        for i in range(len(IDs)):
            el = str(IDs[i])
            time.sleep(0.4)
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
            # write to file. Replace special characters in the strains. If no strain/genome information is present write ""
            f.write(el + "\t" + Names[i] + "\t" +
                    (str(Strains[i]).replace(u"\u2010","-").replace(u"\u2206", "D").replace(u"\u6708", "").replace(u"\u65e5", "").replace(u"\u0425", "X").replace(u"\u2212", "-")
                    if str(Strains[i]) else "") + "\t" +  str(Temps[i]) + "\t" + Superkingdom + "\t" + Phylum + "\t" +
                    Class + "\t" + Order + "\t" + Family + "\t" + Genus + "\t" +
                    (Genomes[i] if not pd.isnull(Genomes[i]) else "") + "\n")
            f.flush()

