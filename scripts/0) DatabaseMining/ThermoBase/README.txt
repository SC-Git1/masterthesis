Data was downloaded from http://togodb.org/db/thermobase with reference:
DiGiacomo, J., McKay, C., & Davila, A. (2022). 
ThermoBase: A database of the phylogeny and physiology of thermophilic and hyperthermophilic organisms. 
In W. J. Brazelton (Ed.), PLOS ONE (Vol. 17, Issue 5, p. e0268253). Public Library of Science (PLoS). https://doi.org/10.1371/journal.pone.0268253

# |  Script or -- action --                       | Output file
-------------------------------------------------------------------------------------------------
1  |  -- download data --                         | ThermoBase_ver_1.0_2022.txt
2a | preprocess1.py                               | df_preprocess1.tsv, CorrectIDsThermoBase.txt
2b | -- manual correction of NCBI Taxonomy IDs -- | CorrectIDsThermoBase_man.txt
2c | preprocess2.py                               | df_preprocessed.tsv
3 |  Lineage.py                                   | NCBI_Annotated_ThermoBase.tsv
-------------------------------------------------------------------------------------------------
