import numpy as np
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

if __name__ == '__main__':
    dfaci = pd.read_csv("aciDB.tsv", sep = "\t", header = 0)
    # print(len(dfaci)) = 600
    dfaci.rename(columns = {'temp_associated':'Temp', 'access_id':'Genome', 'name':'Name', 'strains':'Strain'}, inplace = True)
    dfaci = dfaci[dfaci["Temp"].notna()]
    dfaci.reset_index(inplace=True)
    print(len(dfaci)) # 420 of the 600 records have a temperature annotation
    TaxNames = dfaci["Name"]
    Strains = dfaci["Strain"]
    Temps = dfaci["Temp"]
    Genomes = dfaci["Genome"]

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    with open("NCBI_aciDB3.tsv", "w") as f:
        f.write("Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "ncbiTaxID" + "\t" + "Genome" + "\n")
        for i in range(len(TaxNames)):
            time.sleep(0.4)
            result = get_taxid_from_taxname(TaxNames[i] + " " + Strains[i].replace("/",""))
            if result == -1:
                result = get_taxid_from_taxname(TaxNames[i])

            if not pd.isnull(Genomes[i]):
                f.write(TaxNames[i] + "\t" + Strains[i] + "\t" + str(Temps[i]) + "\t" + str(result) + "\t" + Genomes[i] + "\n")
                f.flush()
            else:
                f.write(TaxNames[i] + Strains[i] + "\t" + "\t" + str(Temps[i]) + "\t" + str(result) + "\t" + "" + "\n")
                f.flush()
