#!/bin/bash

# create new directories  
mkdir -p ./Proteomes


# The frist argument is a tab-separated file with on each line the assembly accession, genus and superkingdom
cat $1 | while read line; 
do
        Genome=$(echo $line | cut -d$' ' -f1)
	# define filepath to genome
        file="/data1/SophieThesis/genomes/$Genome.fna"
        Genus=$(echo $line | cut -d$' ' -f3)
        Superkingdom=$(echo $line | cut -d$' ' -f4)

# if genome file exists:
        if test -f "$file"; then
	# default genus-specific BLAST databases are available for Enterococcus, Escherichia and Staphylococcus
        prokka --outdir Prokka --force --prefix $Genome --genus $Genus --usegenus --kingdom $Superkingdom --evalue 0.001  $file 
        fi

# move proteins file
mv ./Prokka/$Genome.faa ./Proteomes
done

