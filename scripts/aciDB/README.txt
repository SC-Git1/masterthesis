Data of aciDB is available at https://acidb.cl/ with reference: 
Neira, G., Cortez, D., Jil, J., & Holmes, D. S. (2020). 
AciDB 1.0: a database of acidophilic organisms, their genomic information and associated metadata. 
In P. Luigi Martelli (Ed.), Bioinformatics (Vol. 36, Issue 19, pp. 4970–4971). Oxford University Press (OUP). https://doi.org/10.1093/bioinformatics/btaa638

#  | Script or -- action --  | Output file
---------------------------------------------------------
1  | -- retrieve data --     | aciDB.tsv
2a | ncbiTaxID_aciDB.py      | NCBI_aciDB3.tsv
2b | -- manual annotation -- | NCBI_aciDB3_man.tsv
3  | Taxonomy.py             | NCBI_Annotated_aciDB3.tsv
---------------------------------------------------------
