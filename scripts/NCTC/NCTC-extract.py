import os
import pandas as pd
import time

def getData(i):
    url = "https://www.culturecollections.org.uk/products/bacteria/detail.jsp?refId=NCTC+" + str(i) + "&collection=nctc"
    try:
        dfs = pd.read_html(url)
        dict = dfs[0].set_index(0).to_dict()[1]
        return(dict)
    except IndexError:
        return None


if __name__ == "__main__":
    with open("/content/drive/MyDrive/masterthesis/NCTC_extracted3.txt","w") as f:
        listHeader = ["Species", "Strain", "NCTC_number","Type_Strain","Cond_solid","Cond_liquid"]
        f.write("\t".join(listHeader) + "\n")
        # all NCTC numbers seem to be within the range 0-15000
        for i in range(15000):
            time.sleep(0.2)
            species = ""
            family = ""
            NCTC_number = ""
            Type_Strain = ""
            Cond_solid = ""
            Cond_liquid = ""
            Other_Collection_No = ""
            Whole_genome = ""
            Annotated_Genome = ""
            strain = ""
            answer = getData(i)

            # if data is available
            if answer is not None:
                if "Current Name:" in answer:
                    species = answer["Current Name:"]
                if "Original Strain Reference:" in answer:
                    strain = answer["Original Strain Reference:"]
                if "NCTC Number:" in answer:
                    NCTC_number = answer["NCTC Number:"]
                # extract if the record is of a type strain
                if "Type Strain:" in answer:
                    Type_Strain = answer["Type Strain:"]
                # extract growth conditions on both solid and liquid media
                if "Conditions for growth on solid media:" in answer:
                    Cond_solid = answer["Conditions for growth on solid media:"]
                if "Conditions for growth on liquid media:" in answer:
                    Cond_liquid = answer["Conditions for growth on liquid media:"]

                text = species + "\t" + strain + "\t" + NCTC_number + "\t" + Type_Strain + "\t" + Cond_solid + "\t" \
                       + Cond_liquid + "\n"
                # replace special characters, because the NCBI API for Taxonomy ID annotation (next step) does not accept them as input anyway
                text = text.replace(u'\u2082',"2").replace(u"\uFFFD", "?")
                f.write(text)
                f.flush()
                os.fsync(f.fileno())
            else:
                continue
