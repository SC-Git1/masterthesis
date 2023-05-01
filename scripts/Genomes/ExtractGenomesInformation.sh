#!/bin/bash
# This script takes one argument that should be a file containing the NCBI Taxonomy IDs that you want to extract genome information for separated by a newline character 
IDs=$(cat $1)

for el in $IDs
do	
	# try to extract a reference genome 
	GCF=$(datasets summary genome taxon $el --reference | jq '.reports[].accession')
	
	# if no reference is available, try to extract all genomes annotated with the ID
	if [[ -z "$GCF" ]]
	then 
		GCF=$(datasets summary genome taxon $el | jq '.reports[].accession')
		
		# if no genomes are available, set all variables to empty strings
		if [[ -z "$GCF" ]]
		then
			GCF=""
			level=""
			assembly="" 
		# else, extract the 'level' of completeness and the assembly		
		else
			level=$(datasets summary genome taxon $el | jq '.reports[].assembly_info.assembly_level')
			assembly=$(datasets summary genome taxon $el | jq '.reports[].assembly_info.assembly_name')
		fi
	
	# if a reference genome exists, extract the 'level' of completeness and the assembly	
	else	
		level=$(datasets summary genome taxon $el --reference | jq '.reports[].assembly_info.assembly_level')
		assembly=$(datasets summary genome taxon $el --reference | jq '.reports[].assembly_info.assembly_name')
	fi
	
	# write to the output file 'GenomesNCBILevel.txt'
	outID="$el $GCF $level $assembly" 
	echo $outID >> GenomesNCBILevel.txt
done
