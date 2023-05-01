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
    # import data
    df = pd.read_csv("NCTC_extracted_withTemp.tsv", delimiter="\t", header=0, index_col=False)

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    TaxNames = df['Species']
    Strains = df["Strain"]
    Source_IDs = df["Source_ID"]
    Temps = df['Temp']

    with open("ncbiTaxID_NCTC.tsv", "w") as f:
        # header
        f.write("Species" + "\t" + "Strain" + "\t" + "Source_ID" + "\t" + "Temp" + "\t" + "ncbiTaxID" + "\n")
        for i in range(len(TaxNames)):
            print(i)
            time.sleep(0.4)
            # if strain info availbale, try that. Else: try to find a match with the species name
            result = get_taxid_from_taxname((TaxNames[i] + (" " + str(Strains[i]) if Strains[i] else "")).replace("/", " "))
            # if no match on the strain level, try species name
            if (result == -1) and Strains[i]:
                result = get_taxid_from_taxname(TaxNames[i])

            f.write(TaxNames[i] + "\t" + (str(Strains[i]) if Strains[i] else "") + "\t" + Source_IDs[i] + "\t" +
                    str(Temps[i]) + "\t" + str(result) + "\n")
            f.flush()
