This folder stores all files used in the accession number extraction, filtering and genome download for the NCBI Taxonomy ID level. The same workflow was applied on the species level for those entries without a genome after this step. The final file for the species level can be found here as "NewGenomesSpecies.tsv"

-------------------------------------------------------------
# | Script or -- action --       | Output file
-------------------------------------------------------------
1 | ExtractGenomesInformation.sh | GenomesNCBILevel.tsv
2 | GenomesParsedLevel1.py       | GenomesParsedLevel1.tsv
3 | FilterGenomesANI.py          | GenomesApprovedLevel1.tsv
4 | FilterGenomesCompleteness.py | NewGenomes.txt
-------------------------------------------------------------
