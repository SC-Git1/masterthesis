"""
This script writes the synonyms and their NCBI Taxonomy IDs present in the names.dmp file to a .tsv file
"""

# import data
dmp = open("names.dmp", "rb")

with open("synonyms.tsv", "w") as f_out:
    f_out.write("ncbiTaxID" + "\t" + "Synonym" + "\n")
    with open("names.dmp", "r") as f_in:
        lines = f_in.readlines()
        # len(lines) = 3576752
        for i in range(len(lines)):
            line = lines[i]
            fields = [x.strip() for x in line.split("	|")]
            if fields[3] == "synonym":
                f_out.write(str(fields[0]) + "\t" + str(fields[1]) + "\n")
                f_out.flush()

