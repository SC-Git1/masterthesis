#!/usr/bin/python3


## Note: this script takes one input that is a file with all assembly accessions separated by '\n'


from transformers import BertTokenizer, BertModel
import re
import numpy as np
import sys
import os
import time
from Bio import SeqIO
from more_itertools import chunked


def get_list_of_items(inFile):
    fasta_sequences = SeqIO.parse(open(inFile),'fasta')
    sequences = []

    for fasta in fasta_sequences:
        name, sequence = fasta.description, str(fasta.seq)
        if "ribosomal" in name:
            sequences.append(sequence)

    return sequences

def Task(sequences):

	# only GPUs support half-precision currently; if you want to run on CPU use full-precision (not recommended, much slower)
	#model.full() if device=='cpu' else model.half()

	sequence_examples = [" ".join(list(re.sub(r"[UZOB]", "X", sequence))) for sequence in sequences]

	# get representation
	input_ids = tokenizer.batch_encode_plus(sequence_examples, add_special_tokens=True, padding=True, return_tensors="pt")

	ids = input_ids["input_ids"]

	attention_mask = input_ids['attention_mask']

	emb_protein = model(ids)[0]
	emb_protein = emb_protein.detach().numpy()
	emb_protein = np.asarray(emb_protein)

	features = []
	for seq_num in range(len(emb_protein)):
    		seq_len = (attention_mask[seq_num] == 1).sum()
    		seq_emd = emb_protein[seq_num][1:seq_len-1]
    		seq_emd = np.mean(seq_emd, axis = 0)
    		features.append(seq_emd)

	return features


# read in the assembly accessions
inFile = sys.argv[1]
current_dir = os.getcwd()
filepath = os.path.join(current_dir, inFile)

with open(filepath, "r") as f:
        proteomesList = f.readlines()

# initialize the model
tokenizer = BertTokenizer.from_pretrained('Rostlab/prot_bert_bfd', do_lower_case=False)
model = BertModel.from_pretrained("Rostlab/prot_bert_bfd").eval()


# open the output file
with open("ProtTransOut.txt","a") as f_out:

	for prot in proteomesList:
		start_time = time.time()
		Accession = str(prot.replace("\n", ""))
		print(Accession)
                
		# Assign the variable protFile to the location of the fasta file with the predicted proteome for the assembly accession
		protFile = "/home/r0745770/Downloads/Proteomes/" + Accession  + ".faa"
		sequences = get_list_of_items(protFile)

		# calculate the embedding for each protein
		end_emd = []
		for batch in chunked(sequences, 1):
			end_emd.append(Task(batch))

		# calculate the mean embedding over the proteome
		end_emd = np.mean(end_emd, axis = 0)

		# output representation to file
		f_out.write(Accession + "\t")
		for line in end_emd[0]:
			f_out.write(str(line) + "\t")

		f_out.write("\n")
		f_out.flush()
		print("--- %s seconds ---" % (time.time() - start_time))
