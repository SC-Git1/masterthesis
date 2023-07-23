This folder contains the files and scripts created and used in web scraping of the Culture Collection University of Gothenburg (https://www.ccug.se/)
The workflow is (with the output file of each step equal to the input file of the next step):

#  |  Script or -- action --   | Output file
---------------------------------------------------------
1  |  Extract_records.py       | Records.tsv
2  |  data_cleaning.py         | CCUG_info2.tsv
3a |  getNCBITaxonID.py        | NCBITaxID_CCUG.tsv
3b |  -- manual annotation --  | NCBITaxID_CCUG_man.tsv
4  |  Lineage.py               | NCBI_Annotated_CCUG.tsv
---------------------------------------------------------
