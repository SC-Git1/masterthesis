
from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient
import pandas as pd
import time
import re

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
    df = pd.read_csv("NIES_extracted5.tsv", delimiter="\t", header=0, index_col=False, encoding='cp1252')
    # print(len(df)) -> the number of extracted records is 3126

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    TaxNames = df['Name']
    Temps = df['Temp']
    SourceIDs = df['Source_ID']
    Strains = df["Strain"]

    with open("ncbiTaxID_NIES5.tsv", "w", encoding = "latin1") as f:
        f.write("Source_ID" + "\t" + "Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "ncbiTaxID" + "\n")
        for i in range(len(TaxNames)):
            time.sleep(0.4)
            ### extract the NCBI Taxonomy ID
            # Previously observed is that, in the case of NIES, the strains are seldomly helpful in NCBI Taxonomy annotation
            # However, a lot of names contain the NIES Strain number (starting with "NIES-" = Source_ID values)
            result = get_taxid_from_taxname(TaxNames[i] + " " + SourceIDs[i])
            # if no match on the strain level, try the species name
            if result == -1:
                result = get_taxid_from_taxname(TaxNames[i])

            ### extract the temperature
            # the format is 'T1 (T2) C' with T1 = culture condition temperature, and T2 = preculture condition temperature.
            # Here, only extract T1 i.e., the culture condition temperature
            temp = re.search(r'([0-9]*)\s', Temps[i]).group()
            f.write(SourceIDs[i] + "\t" + TaxNames[i] + "\t" + str(Strains[i]) + "\t" + str(temp) + "\t" + str(result) + "\n")
            f.flush()


