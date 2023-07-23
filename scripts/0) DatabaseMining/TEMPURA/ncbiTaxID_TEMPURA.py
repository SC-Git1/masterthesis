from ncbi.datasets import TaxonomyApi
from ncbi.datasets.openapi import ApiClient
import pandas as pd
import time


def get_taxid_from_taxname(taxname):
    # returns an integer (-1) or a string
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
    dfTempura = pd.read_csv("200617_TEMPURA.tsv", delimiter="\t", header=0, index_col=False)
    dfTempura.rename(columns={"taxonomy_id": "ncbiTaxID", "genus_and_species": "Name", "Topt_ave": "Temp",
                              "assembly_or_accession": "Genome", "strain": "Strain"}, inplace=True)

    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    IDs = dfTempura["ncbiTaxID"]
    Temps = dfTempura['Temp']
    Genomes = dfTempura['Genome']

    TaxNames = dfTempura['Name']
    # remove trailing quotations (") from the name if present
    TaxNames = [el.replace("\"", "") for el in TaxNames]

    Strains = dfTempura["Strain"]
    # Replace special characters in strain names. Replace non-existent strains with ""
    Strains = [(str(el).replace(u"\u2010","-").replace(u"\u2206", "D").replace(u"\u6708", "").replace(u"\u65e5", "").replace(u"\u0425", "X").replace(u"\u2212", "-").replace(u"\u2013","-").replace("\"", "")
                    if el else "") for el in Strains]

    with open("ncbiTaxID_TEMPURA.tsv", "w", encoding = "latin1") as f:
        # header
        f.write( "Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "ncbiTaxID" + "\t" + "Genome" + "\n")
        for i in range(len(TaxNames)):
            time.sleep(0.4)
            # try to get the NCBI Taxonomy ID on the strain level
            result = get_taxid_from_taxname((TaxNames[i] + " " + str(Strains[i])).replace("/", " "))
            # NCBI names contain 'sp.' instead of 'sp'
            if (result == -1) & (" sp" in TaxNames[i]):
                result = get_taxid_from_taxname((TaxNames[i] + " " + str(Strains[i])).replace(" sp", " sp.").replace("/", " "))
            # if no ID can be found on the strain level, try species
            if result == -1:
                result = get_taxid_from_taxname(TaxNames[i])
            # if no genome is provided, write "" to file
            if pd.isnull(Genomes[i]):
                f.write(TaxNames[i] + "\t" + str(Strains[i]) + "\t" + str(Temps[i]) + "\t" + str(result) +
                        "\t" + "" + "\n")
            else:
                f.write(TaxNames[i] + "\t" + str(Strains[i]) + "\t" + str(Temps[i]) + "\t" + str(result) + "\t" +
                        Genomes[i] + "\n")
            f.flush()
