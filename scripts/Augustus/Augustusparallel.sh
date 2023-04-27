#!/bin/bash
# create directories for the proteomes and GFF files
mkdir -p /data1/SophieThesis/AugustusAnnotation/parProteomes
mkdir -p /data1/SophieThesis/AugustusAnnotation/parGFFs

# directory that contains the script 'run_augustus_parallel' (script from https://github.com/Daniel-Ze/augustus_parallel)
WorkDir="/data1/SophieThesis/Augustus/parallel"

# the inputfile should have the same format as the 'ClosestIdentifier.tsv' file
cat $1 | while read line; 
do
        Genome=$(echo $line | cut -d$' ' -f1)
        file="/data1/SophieThesis/genomes/$Genome.fna"
        Identifier=$(echo $line | cut -d$' ' -f3)

# if file with genome exists:
       if test -f "$file"; then
	  # get the number of sequences in the fasta file of the genome
        nfasta=$(grep -E '^>' $file | wc -l)
	# run augustus in parallel
	run_augustus_parallel -f $file -j $nfasta -c 4 -s $Genome -o $WorkDir -p '--species='"$Identifier"', --protein=on, --codingseq=off' 2>/dev/null

       fi
	
	# move the .aa (proteome) and .gff3 file into their respective destination folders
	mv $WorkDir/$Genome.fna.aug3.aa /data1/SophieThesis/AugustusAnnotation/parProteomes
	mv $WorkDir/$Genome.fna.aug.gff3 /data1/SophieThesis/AugustusAnnotation/parGFFs
	
	# remove redundant output files and the temporary directory
	rm $WorkDir/$Genome.fna.aug3.codingseq
	rm $WorkDir/$Genome.fna.aug3.cdsexons
	rm  -R /data1/SophieThesis/Augustus/parallel/tmp


done
