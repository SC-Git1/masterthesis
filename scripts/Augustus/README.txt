A list of pre-trained species for Augustus can be found for your installed Augustus version at /Augustus/config/species
The file "speciesAugustusUpdated.txt" contains a filtered list (redundant entries and templates were removed) of the available species in version ... .
The table below gives an overview of the workflow.

----------------------------------------------------------------------------------------------
#  | Script or -- action --                            | Output file
----------------------------------------------------------------------------------------------
1  | -- get a list of available pre-trained species -- | speciesAugustusUpdated.txt
2  | getTaxidAugustus.py                               | NCBI_AugustusUpdated_TaxIDs.tsv
3  | -- manual annotation --                           | NCBI_AugustusUpdated_TaxIDs_man.tsv
4  | LineageAugustus.py                                | NCBI_Annotated_AugustusUpdated.tsv
4b | -- merge previously retireved data --             | NCBI_Annotated_EukaryoticGenomes.tsv
5  | AssignToClosestIdentifier.py                      | ClosestIdentifier.tsv
----------------------------------------------------------------------------------------------



