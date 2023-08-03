import pandas as pd
import time
from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient

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
    # import data
    df = pd.read_csv("speciesAugustusUpdated.txt", sep="\t", header=0)

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    TaxNames = df['Name']
    Identifiers = df["Identifier"]

    with open("NCBI_AugustusUpdated_TaxIDs.tsv", "w") as f:
        # header
        f.write("Name" + "\t" + "Identifier" + "\t" + "ncbiTaxID" + "\n")
        for i in range(len(TaxNames)):
            time.sleep(0.4)
            result = get_taxid_from_taxname(TaxNames[i])
            f.write(TaxNames[i] + "\t" + Identifiers[i] + "\t" + str(result) + "\n")
            f.flush()

