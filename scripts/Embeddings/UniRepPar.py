#!/usr/bin/python3


## Note: this script takes one input that is a file with all assembly accessions separated by '\n'
## This is the example for the ribosomal proteins. For other conserved protein subsets read the in code comments


from jax_unirep import get_reps
from Bio import SeqIO
import time
import sys
import numpy as np
import pandas as pd
import os
import random
from os import path


def actual_task(sequences):
    h_avg, h_final, c_final = get_reps(sequences)
    return h_avg

def get_list_of_items(inFile):
    sequences = []

    if path.exists(inFile):
        fasta_sequences = SeqIO.parse(open(inFile),'fasta')

    ## Note: For selection of a random subset of proteins, use the line below, else use the for loop.
    #sequences = [str(fasta.seq) for fasta in random.sample(list(fasta_sequences),50)]

        for fasta in fasta_sequences:
            name, sequence = fasta.description, str(fasta.seq)
	    ## Note: comment out the if loop in case of all proteins
            if "ribosomal" in name:
    	        sequences.append(sequence)
    return sequences

if __name__ == "__main__":
    
    random.seed(5)
    
    # read in the assembly accessions from the file in the current
    inFile = sys.argv[1]
    current_dir = os.getcwd()
    filepath = os.path.join(current_dir, inFile)

    with open(filepath, "r") as f:
        	proteomesList = f.readlines()

    ## open output file
    with open("Ribosomal_all.txt","a") as f_out:
                
        	for prot in proteomesList:
	            start_time = time.time()
		    Accession = str(prot.replace("\n", ""))
		    print(Accession)
		    
                    # Assign the variable protFile to the location of the fasta file with the predicted proteome for the assembly accession
                    protFile = "/home/r0745770/Documents/AllProteomes/" + Accession  + ".faa"
		    sequences = get_list_of_items(protFile)
		    if len(sequences) > 0:
                        # determine set of proteins and calculate the average embedding over the proteins
		        result = actual_task(sequences)
		        oneArray = np.vstack(result)
		        print(oneArray.shape)
		        meanh = np.mean(result, axis=0)

		        f_out.write(Accession + "\t" + str(len(sequences)) + "\t")
		        for line in meanh:
			        f_out.write(str(line) + "\t")

		    f_out.write("\n")
		    f_out.flush()
		    print("--- %s seconds ---" % (time.time() - start_time))
