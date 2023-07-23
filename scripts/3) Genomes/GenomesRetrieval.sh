#!/bin/bash

## NOTE: 
# this script uses the working directory. Prior to running, make sure no folder called 'ncbi_dataset' exists.
# the CLI tool datasets can be downloaded from https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/ or GitHub (https://github.com/ncbi/datasets).

# create a new directory
mkdir -p genomes

# The first argument is a file that contains the accession numbers separated by a newline character
IDs=$(cat $1) 

for el in $IDs
do
	# define the path of the folder and files after download
	elFile="./ncbi_dataset/data/$el/*"
	elDir="./ncbi_dataset/data/$el"
	
	# Download the folder and get the genome .fna file
	./datasets download genome accession $el --include genome
	unzip ncbi_dataset.zip
	mv $elFile "./ncbi_dataset/data/$el/$el.fna"
	cp $elFile ./genomes

	# clean the working directory
	rm -R ./ncbi_dataset
	rm -R ./ncbi_dataset.zip
done
