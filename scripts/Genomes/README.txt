This folder stores all files used in the accession number extraction, filtering and genome download for the NCBI Taxonomy ID level. The same workflow was applied on the species level for those entries without a genome after this step. The final file for the species level with all new genomes can be found here as "NewGenomesSpecies.tsv". All lineage information was retreived with the TaxonomyApi provided with the ncbi-datasets-pylib package (https://www.ncbi.nlm.nih.gov/datasets, version 14.25.1).

-------------------------------------------------------------
# | Script or -- action --       | Output file
-------------------------------------------------------------
1 | ExtractGenomesInformation.sh | GenomesNCBILevel.tsv
2 | GenomesParsedLevel1.py       | GenomesParsedLevel1.tsv
3 | FilterGenomesANI.py          | GenomesApprovedLevel1.tsv
4 | FilterGenomesCompleteness.py | NewGenomes.txt
5 | Lineage.py | 
-------------------------------------------------------------
