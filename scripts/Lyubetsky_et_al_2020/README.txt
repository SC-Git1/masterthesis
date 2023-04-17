Files and scripts for the processing of the OGT data found in the supplementary material (Supplementary Spreadsheet.xlsx) of:

Lyubetsky, V. A., Zverkov, O. A., Rubanov, L. I., & Seliverstov, A. V. (2020). 
Optimal Growth Temperature and Intergenic Distances in Bacteria, Archaea, and Plastids of Rhodophytic Branch. 
In BioMed Research International (Vol. 2020, pp. 1–10). Hindawi Limited. https://doi.org/10.1155/2020/3465380

The workflow is (with the output file of each step equal to the input file of the next step):

#  | Script or -- action --           | Output file
---------------------------------------------------------
1  | --retrieve supplementary data -- | Records.tsv
2a | getNCBITaxonID_Lyubetsky.py      | ncbiTaxID_Lyubetsky2020.tsv
2b | -- manual annotation --          | ncbiTaxID_Lyubetsky2020_man.tsv
3  | lineage_Lyubetsky2020.py         | NCBI_Annotated_Lyubetsky2020.tsv
