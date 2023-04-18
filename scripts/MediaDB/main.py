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

    dfOrg = pd.read_csv("MediaDB_organisms.txt", header=0, delimiter="\t", encoding="latin1")
    dfGD = pd.read_csv("MediaDB_growth_data.txt", header=0, delimiter="\t", encoding="latin1")
    df = pd.merge(dfGD, dfOrg, on="strainID", how="inner")

    print(len(df))  # 779
    ## remove those w/o temp
    df = df[~pd.isnull(df["Temperature_C"])]
    df.reset_index(inplace=True)
    print(len(df)) # 649
    ## replace "-" with NA for strains
    df.loc[df['Strain'] == "-", 'Strain'] = ""

    df["Name"] = df["Genus"] + " " + df["Species"]

    Names = df["Name"]
    Strains = df["Strain"]
    Temps = df["Temperature_C"]
    Source_IDs = df["growthID"]

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

        with open("MediaDB_taxid.tsv", "w", encoding="latin1") as f:
            f.write("Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "ncbiTaxID" + "\t" + "Source_ID" + "\n")
            for i in range(len(df)):
                el = str(Names[i])
                print(i)
                time.sleep(0.4)

                result = get_taxid_from_taxname((el  + " " + Strains[i]).replace("/"," "))
                if result == -1:
                    result = get_taxid_from_taxname(el)

                f.write(el + "\t"  + Strains[i] + "\t" + str(Temps[i]) + "\t" + str(result) + "\t" + str(Source_IDs[i]) + "\n")
                f.flush()