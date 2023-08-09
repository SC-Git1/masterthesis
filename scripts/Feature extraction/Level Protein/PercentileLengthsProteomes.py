#!usr/bin/python3

from Bio import SeqIO
import os
import numpy as np


if __name__ == '__main__':

	# Set inFile to a file with all assembly accessions for which a proteome exists
	
	inFile = "UniqueCorrGenomes.tsv"
	current_dir = os.getcwd()
	filepath = os.path.join(current_dir, inFile)

	with open(filepath, "r") as f:
		proteomesList = [line.replace('\n','') for line in f.readlines()]

	with open('Perc_all.tsv','w') as out_file:

		# header
		out_file.write('Genome'+'\t'+'Perc1'+'\t'+'Perc5'+'\t'+'Perc10'+'\t'+'Perc20'+'\t'+'Perc30'+'\t'+'Perc40'+'\t'+'Perc50'+'\t'+'Perc60'+'\t'+'Perc70'+'\t'+'Perc80'+'\t'+ 'Perc90'+'\t'+'Perc95'+'\t'+'Perc99'+'\n')

		for proteome in proteomesList:
			# read in the predicted proteome
			protFile = '/home/r0745770/Documents/AllProteomes/' + proteome + '.faa'
			out_file.write(proteome + '\t')

			if os.path.exists(protFile):
				# read in the fasta sequences
				fasta_sequences = SeqIO.parse(open(protFile),'fasta')

				# calculate the length at each percentile
				lengths = [len(record) for record in fasta_sequences]
				for perc in [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]:
					out_file.write(str(np.percentile(lengths,perc)) + '\t')
					out_file.flush()
			# write to output
			out_file.write('\n')
