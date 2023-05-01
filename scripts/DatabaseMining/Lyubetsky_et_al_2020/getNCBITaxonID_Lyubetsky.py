import pandas as pd
from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient
import time

def get_taxid_from_taxname(taxname):
    # returns integer
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
    dfLyubesky2020 = pd.read_csv("Lyu_2020.tsv", header = 0, sep = "\t")

    TaxNames = dfLyubesky2020['Name']
    Temps = dfLyubesky2020["Temp"]
    Strains = dfLyubesky2020["Strain"]

    with open("ncbiTaxID_Lyubetsky2020.tsv", "w") as f:
        f.write("ncbiTaxID" + "\t" + "Name" + "\t" + "Strain" + "\t" + "Temp" + "\n")

        for i in range(len(TaxNames)):
            result = -1
            txname = TaxNames[i]
            time.sleep(0.4)
            # if strain information is available
            if not pd.isnull(Strains[i]):
                print(Strains[i])
                result = get_taxid_from_taxname((txname + " " + Strains[i]).replace("/", " "))
            # if no taxid could be found on the strain level, try species
            if result == -1:
                result = get_taxid_from_taxname(txname)

            f.write(str(result) + "\t" + txname + "\t" + str(Strains[i]) + "\t" + str(Temps[i]) + "\n")
            f.flush()


