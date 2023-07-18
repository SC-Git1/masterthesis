from unipressed import UniprotkbClient
import sys


# Note: the same workflow was used for Archaea and Bacteria

with open("Swiss-Prot_LengthDistrEuk.tsv", "w") as f:
    # write header
    f.write("Length (>=)" + "\t" + "Absolute Count" + "\n")

    # 40,000 is based on an initial look at UniProtKB
    for length in list(range(0,40000,100)):
        # initialize
        counter = 0

        query = "(taxonomy_name:Eukaryota) AND (length:[" + str(length) + " TO *]) AND (reviewed:true)"

        for record in UniprotkbClient.search(query = query).each_record():
            counter += 1

        # if no protein has a length >= 'length', end the program
        if counter == 0:
            sys.exit(0)

        # write to file
        f.write(str(length) + "\t" + str(counter) + "\n")
        f.flush()