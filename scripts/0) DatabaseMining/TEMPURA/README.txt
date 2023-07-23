The file "200617_TEMPURA.tsv" contains data downloaded from http://togodb.org/db/tempura with reference publication: 
Sato, Y., Okano, K., Kimura, H., & Honda, K. (2020). 
TEMPURA: Database of Growth TEMPeratures of Usual and RAre Prokaryotes. In Microbes and Environments (Vol. 35, Issue 3, p. n/a). 
Japanese Society of Microbial Ecology. https://doi.org/10.1264/jsme2.me20074

The database contains some erroneous strain names because of conversion of number to date e.g. Pseudomonas kribbensis (TaxId: 1628086) 
has strain name "Feb-46", although, according to the NCBI Taxonomy database, this should be "46-2". Records containing abbreviations of months were manually inspected and the strain name was corrected if necessary.

#  |  Script or -- action -- | Output file
-----------------------------------------------------------
1  | -- download data --     | 200617_TEMPURA.tsv
2a |  ncbiTaxID_TEMPURA.py   | ncbiTaxID_TEMPURA.tsv
2b | -- manual annotation -- | ncbiTaxID_TEMPURA_man.tsv
4  | lineage_TEMPURA.py      | NCBI_Annotated_Tempura4.tsv
-----------------------------------------------------------


