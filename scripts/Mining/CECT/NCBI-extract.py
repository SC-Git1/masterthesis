from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient
import pandas as pd
import time


def get_taxid_from_taxname(taxname):

    taxid = -1
    data = taxon_api.tax_name_query(taxon_query=taxname)
    try:
        for taxon in data.sci_name_and_ids:
            if taxon.sci_name == taxname:
                taxid = taxon.tax_id
                break
    except:
        pass
    return taxid

if __name__ == "__main__":
    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)
        
    # import data
    df = pd.read_csv("CECT_with_Genome2.tsv", delimiter="\t", header=0, index_col=False)
    # print(len(df)) # 7992
    TaxNames = df['Name']
    Source_IDs = df["Source_ID"]
    Temps = df["Temp"]
    Strains = df["Strain"]
    Genomes = df["Genome"]

    with open("NCBI_CECT_TaxID2.tsv", "w", encoding = "latin1") as f:
        # header
        f.write( "Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "Source_ID" + "\t" + "ncbiTaxID" + "\t" + "Genome" + "\n")
        
        for i in range(len(TaxNames)):
            time.sleep(0.4)
            # try match for strain level
            result = get_taxid_from_taxname((TaxNames[i] + " " + str(Strains[i])).replace("/", " "))
            # if ono match could be found on the strain level, try to correct names containing ' sp'
            if (result == -1) & (" sp" in TaxNames[i]):
                result = get_taxid_from_taxname((TaxNames[i] + " " + str(Strains[i])).replace(" sp", " sp.").replace("/", " "))
            # else: try to extract TaxId on the species level
            if result == -1:
                result = get_taxid_from_taxname(TaxNames[i])
            
            # write to file
            if pd.isnull(Genomes[i]):
                f.write(TaxNames[i] + "\t" + str(Strains[i]) + "\t" + str(Temps[i]) + "\t" + Source_IDs[i] + "\t" + str(result) +
                        "\t" + "" + "\n")
            else:
                f.write(TaxNames[i] + "\t" + str(Strains[i]) + "\t" + str(Temps[i]) + "\t" + Source_IDs[i] + "\t" + str(
                    result) + "\t" + Genomes[i] + "\n")
            f.flush()