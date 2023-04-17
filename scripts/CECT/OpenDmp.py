import io
import pandas as pd

dmp = open("names.dmp", "rb")

# source: https://github.com/ebi-jdispatcher/taxonomy-resolver/blob/d2b224ad999f5b706e0df9f835570c3d2977e178/taxonresolver/utils.py

# file of those having a synonym
with open("synonyms.tsv", "w") as f_out:
    f_out.write("ncbiTaxID" + "\t" + "Synonym" + "\n")
    with open("names.dmp", "r") as f_in:
        lines = f_in.readlines()
        # len(lines) = 3576752
        for i in range(3576752):
            line = lines[i]
            fields = [x.strip() for x in line.split("	|")]
            if fields[3] == "synonym":
                f_out.write(str(fields[0]) + "\t" + str(fields[1]) + "\n")
                f_out.flush()

