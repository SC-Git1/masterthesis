This folder contains the files and scripts created and used in web scraping of the Sapnish Type Culture Collection (https://www.uv.es/uvweb/spanish-type-culture-collection/en/spanish-type-culture-collection-1285872233521.html)
Note: genome accessions are extracted, but only for use in manual annotation.

(add some ref info)

#  |  Script or -- action --   | Output file
---------------------------------------------------------
1  |  extract_CECT.py          | CECT_with_Genome2.tsv
2  |  NCBI-extract.py	       | NCBI_CECT_TaxID2.tsv
3a |  BacDiveToAnnotate.py     | ncbiTaxID_CECT2WithBacDive.tsv
3b |  -- manual annotation --  | ncbiTaxID_CECT2_man.tsv
4  |  NCBILineage.py           | NCBI_Annotated_CECT2.tsv
---------------------------------------------------------
