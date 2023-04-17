import pandas as pd
import bacdive
import time


def AnnotateWithBacDive(strains, sourceIDs):
    IDs = []
    # strains and sourceIDs are pd.Series objects
    for i in strains.index:
        strain = strains.loc[[i]].values[0]
        sourceID = sourceIDs.loc[[i]].values[0]
        # initialize the ID to -1
        Id_Retrieved = -1
        # If a strain exists, search for it as if it is a culture collection number, because some are of this format
        # e.g., NCTC 4553 for CECT 1
        if not pd.isnull(strain):
            result = client.search(culturecolno=strain)
            try:
                for hit in client.retrieve():
                    if isinstance(hit.get("General").get("NCBI tax id"), dict):
                        Id_Retrieved = hit.get("General").get("NCBI tax id").get("NCBI tax id")

                    elif isinstance(hit.get("General").get("NCBI tax id"), list):
                        # If the type is 'list', generally both species and strain ID are returned.
                        # The assert statement checks if the second value is indeed of the level 'strain'
                        assert hit.get("General").get("NCBI tax id")[1].get("Matching level") == "strain"
                        Id_Retrieved = hit.get("General").get("NCBI tax id")[1].get("NCBI tax id")
            except:
                pass
        try:
            if Id_Retrieved == -1:
                result = client.search(culturecolno=sourceID)
                for hit in client.retrieve():
                    if isinstance(hit.get("General").get("NCBI tax id"), dict):
                        Id_Retrieved = hit.get("General").get("NCBI tax id").get("NCBI tax id")

                    elif isinstance(hit.get("General").get("NCBI tax id"), list):
                        # If the type is 'list', generally both species and strain ID are returned.
                        # The assert statement checks if the second value is indeed of the level 'strain'
                        assert hit.get("General").get("NCBI tax id")[1].get("Matching level") == "strain"
                        Id_Retrieved = hit.get("General").get("NCBI tax id")[1].get("NCBI tax id")

        except:
            pass
        IDs.append(str(Id_Retrieved))
    return IDs

if __name__ == "__main__":
    """
    read in the credentials for BacDive from a file "credentials.txt" containing two lines with the following format:
    email@example.com
    password
    """
    with open("credentials.txt", "r") as f:
        lines = f.readlines()
        email = lines[0].replace("\n", "")
        password = lines[1].replace("\n", "")
    client = bacdive.BacdiveClient(email, password)

    # import data
    df = pd.read_csv("ncbiTaxID_CECT2.tsv", header=0, sep = "\t", encoding="latin1")
    # print(len(df)) -> there are 7992 records
    ncbiTaxIDs = df["ncbiTaxID"]
    Source_IDs = df["Source_ID"]
    Strains = df["Strain"]

    # for all records that have -1 as NCBI Taxonomy ID
    # print(len(df[df["ncbiTaxID"] == -1])) # 1555 records do not have an ncbi Taxonomy ID yet
    # masks all positions
    df.loc[df["ncbiTaxID"].isin([-1]), "ncbiTaxID"] = AnnotateWithBacDive(df[df["ncbiTaxID"].isin([-1])]["Strain"],
                df[df["ncbiTaxID"].isin([-1])]["Source_ID"])

    df.to_csv("ncbiTaxID_CECT2WithBacDive.tsv", sep = "\t", index = False)

