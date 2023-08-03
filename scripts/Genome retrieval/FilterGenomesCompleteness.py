import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == "__main__":
    # import data
    df = pd.read_csv("GenomesApprovedLevel1.tsv", sep ="\t", header = 0)
    # remove the entries without a genome: reduces the number of entries from 23819 to 19205
    df = df[df["Genome"].notna()]

    # initiate an empty pandas dataframe
    dfQL = pd.DataFrame()
    # group by ncbiTaxID
    a = df.groupby(["ncbiTaxID"])
    # for each group, keep only the genomes with the highest available completeness
    for name, group in a:
        # iterate over levels of completeness
        for i in ['Complete Genome', 'Chromosome', 'Scaffold', 'Contig']:
            # if present, subset those and add to dataframe 'dfQL'
            if i in list(group["Quality"]):
                subset = group[group["Quality"] == i]
                dfQL = pd.concat([dfQL, subset])
                break

    # print(len(dfQL)) -> 11871 genomes remain

    # write to file
    dfQL.to_csv("NewGenomes.tsv", sep = "\t", index = False)

