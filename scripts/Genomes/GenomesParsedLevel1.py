import pandas as pd

with open("GenomesNCBILevel.txt", "r") as f:
    lines = f.readlines()
    # This file is space-delimited with the first column containing the ncbiTaxID and all other columns containing
    # information about the genome.
    ncbiTaxIDs = [line.split(" ")[0].replace("\n", "") for line in lines]
    GenomesInfo = [" ".join(line.split(" ")[1:]).replace("\n", "") for line in lines]
    
    # now, split the genome information that consists of three parts: 1) accession number, 2) completeness, and 3) assembly
    GenomesAcc = []
    GenomesQual = []
    GenomesTaxonomy = []
    for i in range(len(GenomesInfo)):
        el = GenomesInfo[i]
        # if there is genome information available
        if el:
            splitted = el.split(" \"")
            # get number of genomes
            nGen = int(len(splitted) / 3)
            # extract info and store in lists
            for j in range(nGen):
                GenomesTaxonomy.append(ncbiTaxIDs[i])
                GenomesAcc.append(splitted[int(j)].replace("\"", ""))
                GenomesQual.append(splitted[int(j + nGen)].replace("\"", ""))
        else:
            # if no genome information is available, store the ncbiTaxID with empty inputs
            GenomesAcc.append("")
            GenomesQual.append("")
            GenomesTaxonomy.append(ncbiTaxIDs[i])

    # create a pandas dataframe
    GenomesParsed = pd.DataFrame()
    GenomesParsed["ncbiTaxID"] = GenomesTaxonomy
    GenomesParsed["Genome"] = GenomesAcc
    GenomesParsed["Quality"] = GenomesQual
    # write to file
    GenomesParsed.to_csv("GenomesParsedLevel1.tsv", sep="\t", index=False)
