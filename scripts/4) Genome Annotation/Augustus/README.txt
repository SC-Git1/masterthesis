A list of pre-trained species for Augustus can be found for your installed Augustus version at /Augustus/config/species
The file "speciesAugustusUpdated.txt" contains a filtered list (redundant entries and templates were removed) of the available species in version 3.5.0.
The table below gives an overview of the workflow.

----------------------------------------------------------------------------------------------
#  | Script or -- action --                            | Output file
----------------------------------------------------------------------------------------------
1  | -- get a list of available pre-trained species --  | speciesAugustusUpdated.txt
2  | getTaxidAugustus.py                                | NCBI_AugustusUpdated_TaxIDs.tsv
3  | -- manual annotation --                            | NCBI_AugustusUpdated_TaxIDs_man.tsv
4  | LineageAugustus.py                                 | NCBI_Annotated_AugustusUpdated.tsv
5  | AssignToClosestIdentifier.py                       | ClosestIdentifier.tsv
----------------------------------------------------------------------------------------------

Since Augustus is quite a slow program, paralllellization was achieved with the script "run_augustus_parallel" written by Daniel-Ze on GitHub (available at https://github.com/Daniel-Ze/augustus_parallel).
Finally, the script Augustusparallel.sh (bash) was used to run Augustus with 'ClosestIdentifier.tsv' as the input file.



