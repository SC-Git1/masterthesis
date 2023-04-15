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
    df = pd.read_csv("AnnotatedWithSpecies_CCUG2.tsv", delimiter="\t", header=0, index_col=False)
    # print(len(df)) #-> 2954 records

    TaxNames = df['Strain']
    Source_IDs = df["CCUG Number"]
    Temps = df["Temp"]

    with open("NCBITaxID_CCUG.tsv", "w") as f:
        f.write("Source_ID" + "\t" + "Name" + "\t" + "Temp" + "\t" + "ncbiTaxID" + "\n")
        for i in range(len(TaxNames)):
            print(i)
            time.sleep(0.4)
            result = get_taxid_from_taxname(TaxNames[i])
            f.write(Source_IDs[i] + "\t" + TaxNames[i] + "\t" + Temps[i] + "\t" + str(result) + "\n")
            f.flush()