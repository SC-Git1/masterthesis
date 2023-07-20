from ete3 import NCBITaxa
import pandas as pd


def treeTaxId(listIDs, outfile):
    # construct the tree
    ncbi = NCBITaxa()
    tree = ncbi.get_topology(listIDs)
    tree.resolve_polytomy(recursive=True)
    tree.write(features=["sci_name"], outfile=outfile)

if __name__ == "__main__":

    # import data
    df = pd.read_csv("All_Input_.tsv", sep = "\t", header = 0)
    df[["ncbiTaxID", "Temp"]].to_csv("TaxIdsProteomes.tsv", sep = "\t", index = False)
    treeTaxId(list(df["ncbiTaxID"]), "TreeProteomes.nw")