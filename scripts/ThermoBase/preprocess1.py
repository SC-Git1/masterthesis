import pandas as pd
import re
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

def FindCorrectTaxID(taxid, taxname, strain):
    # check if the given Taxonomy ID ('taxid') exists
    try:
        time.sleep(0.3)
        data = taxon_api.taxonomy_metadata(taxons=[taxid])
        Taxname = str(data.get("taxonomy_nodes")[0].get("taxonomy").get("organism_name"))
        return taxid

    # If not, try to find it through the Taxonomy API
    except AttributeError:
        time.sleep(0.1)
        # if mulitple strain designations are given, they are usually separated by a comma. First, create a list 'strains'
        strains = strain.split(",")
        # for each strain designation, try to match name + strain
        for i in range(len(strain)):
            result = get_taxid_from_taxname(taxname + (" " + str(strains[i].strip()) if strains else "").replace("/", " "))
            # If a match is found, return it
            if result != -1:
                return result
        # If no matches are found on the strain level, try to match the name
        if result == -1 and strain:
            result = get_taxid_from_taxname(taxname)

        return result


if __name__ == "__main__":
    # import data
    df = pd.read_csv("ThermoBase_ver_1.0_2022.txt", sep = "\t", header = 0, dtype= {"Taxonomic ID":str})
    df = df.rename(columns = {"Taxonomic ID":"ncbiTaxID", "Domain":"Superkingdom", "Avg. Optimum Temp (°C)":"Temp"})

    # remove special character NBSP
    df.loc[df['ncbiTaxID'].str.contains(u"\u00A0", na=False), 'ncbiTaxID'] = df["ncbiTaxID"].str.replace(u"\u00A0", "")
    df.loc[df['Name'].str.contains(u"\u00A0", na=False), 'Name'] = df["Name"].str.replace(u"\u00A0", " ")

    # extract strain from name
    df.loc[~df['Name'].str.contains("Candidatus"), 'Strain'] = df["Name"].str.split().str[2:]
    df.loc[df['Name'].str.contains("sp "), 'Strain'] = df["Name"].str.rsplit("sp ").str[1:]
    df.loc[df['Name'].str.contains("Candidatus"), 'Strain'] = df["Name"].str.split().str[3:]
    df["Strain"] = [re.sub(r"[Ss]train(\s?)", "", ' '.join(v)) for v in df["Strain"]]

    # extract species from name
    df.loc[~df['Name'].str.contains("Candidatus | sp"), 'Name'] = df["Name"].str.split().str[:2]
    df.loc[df['Name'].str.contains("Candidatus", na=False), 'Name'] = df["Name"].str.split().str[:3]
    df.loc[df['Name'].str.contains("sp ", na=False), 'Name'] = df['Name'].str.split(r'(.*sp)\s').str[1]
    df["Name"] = [' '.join(v) if isinstance(v, list)  else v for v in df["Name"]]

    #Extract Genus information
    df["Genus"] = df["Name"].str.split(expand = True)[0]

    # Correct ncbiTaxID
    # these were manually found during exploration of the data
    df.loc[df["ncbiTaxID"] == "65551", "ncbiTaxID"] = "65552"
    df.loc[df["ncbiTaxID"] == "5149", "ncbiTaxID"] = "-1"
    df.loc[df["ncbiTaxID"] == "35719", "ncbiTaxID"] = "-1"
    df.loc[df["ncbiTaxID"] == "129311", "ncbiTaxID"] = "-1"
    df.loc[df["Name"] == "Thermoanaerobacter tengcongensis", "ncbiTaxID"] = "119072"


    # write current df to tsv (before global correction of invalid IDs)
    df.to_csv("df_preprocess1.tsv", sep = "\t", index = False)

    ### correct invalid NCBI Taxonomy IDs
    with ApiClient() as api_client:
        taxon_api = TaxonomyApi(api_client)

    # store all corrected IDs in a new file 'CorrectIDsThermoBase'
    with open("CorrectIDsThermoBase.txt", "w") as f:
        # header
        f.write("ID" + "\t" + "Name" + "\t" + "Strain" + "\n")

        for i in range(len(df["ncbiTaxID"])):
            taxid = df.iloc[i]["ncbiTaxID"]
            taxname = df.iloc[i]["Name"]
            strain = df.iloc[i]["Strain"]
            result = FindCorrectTaxID(taxid, taxname, strain)
            f.write(str(result) + "\t" + taxname + "\t" + (str(strain) if strain else "") + "\n")
            f.flush()


