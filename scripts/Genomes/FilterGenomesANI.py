import pandas as pd

if __name__ == '__main__':
    ## import data
    # ANI report from: https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/ANI_report_prokaryotes.txt
    dfQuality = pd.read_csv("ANI_report_prokaryotes.txt", header=0, sep="\t")
    dfGenomes = pd.read_csv("GenomesParsedLevel1.tsv", header = 0, sep = "\t")

    ## try to map all genomes to their ANI report data if present
    # Note: genomes either start with GCF_ (# genbank-accession) or GCA_ (refseq-accession).

    # First, merge the genome data with the ANI report data based on the GenBank accession
    dfGCA = pd.merge(dfGenomes, dfQuality, how="left", left_on="Genome", right_on="# genbank-accession")
    # subset columns of interest
    dfGCA = dfGCA[['ncbiTaxID', 'Genome', 'Quality', "best-match-status", "taxonomy-check-status"]]
    # Next, try to merge on the RefSeq accession
    dfAll = pd.merge(dfGCA, dfQuality, how="left", left_on="Genome", right_on="refseq-accession")
    # keep the information from the RefSeq match only if the values for 'best-match-status' and 'taxonomy-check-status' are nan)
    dfAll['best-match-status'] = dfAll['best-match-status_x'].fillna(dfAll['best-match-status_y'])
    dfAll['taxonomy-check-status'] = dfAll['taxonomy-check-status_x'].fillna(dfAll['taxonomy-check-status_y'])
    # subset columns of interest
    dfAll = dfAll[['ncbiTaxID', 'Genome', 'Quality', "best-match-status", "taxonomy-check-status"]]
    dfAll.to_csv("GenomesWithStatusSpeciesLevel1.tsv", sep="\t", index=False)

    # keep all entries with taxonomy status OK or nan
    dfApproved = dfAll[(dfAll["taxonomy-check-status"] != "Inconclusive") & (dfAll["taxonomy-check-status"] != "Failed")]
    print(dfApproved["taxonomy-check-status"].head())

    ## Next, remove accession numbers that refer to the same assembly
    DisApprovedCleaned = []

    for Genome in list(dfApproved[dfApproved["Genome"].notna()]["Genome"]):
        # For a GenBank accession number, find the equivalent RefSeq in ANI report (if available) and add the redundant
        # RefSeq accession to the list 'DisApprovedCleaned'.
        if "GCA_" in Genome:
            try:
                index = list(dfQuality["# genbank-accession"]).index(Genome)
                RefseqEquivalent = list(dfQuality["refseq-accession"])[index]
                if (RefseqEquivalent != "na"): DisApprovedCleaned.append(RefseqEquivalent)

            # Ignore those not in the ANI report:
            except ValueError:
                pass
        elif "GCF_" in Genome:
            pass
        # print accessions not starting with GCA_ or GCF_. Result: none are present
        else:
            print(Genome)

    # remove the redundant RefSeq accessions and write to file
    DisApprovedCleaned_df = pd.DataFrame(DisApprovedCleaned)
    dfApproved = dfApproved[~dfApproved["Genome"].isin(DisApprovedCleaned)]
    dfApproved.to_csv("GenomesApprovedLevel1.tsv", sep="\t", index=False)