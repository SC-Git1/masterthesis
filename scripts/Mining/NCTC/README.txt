National Collection of Type Cultures

The complete alfabetical listing of bacteria and mycoplasmas can be found on https://www.culturecollections.org.uk/products/bacteria/browse.jsp. The data was extracted on the 4th of April 2023 and stored in the file "species_avail_in_NCTC_04032023_alphabetical_listing.txt".

#  | Script or -- action --                                | Output file
--------------------------------------------------------------------------------------------------------------------
0  | -- get a list of the number of records per species -- | species_avail_in_NCTC_04032023_alphabetical_listing.txt
1  | NCTC-extract.py                                       | NCTC_extracted3.tsv
2  | checkExtractedData.py                                 | (CountDifferences.tsv)
3  | extractTemps.py                                       | NCTC_extracted_withTemp.tsv
4a | ncbiTaxID.py                                          | ncbiTaxID_NCTC.tsv
4b | -- manual annotation --                               | ncbiTaxID_NCTC_man.tsv
5  | TaxonomyScript.py                                     | NCBI_Annotated_NCTC5.tsv
--------------------------------------------------------------------------------------------------------------------
