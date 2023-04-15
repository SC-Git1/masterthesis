import re
import time
import pandas as pd

"""
The CCUG provides data on all records in their TypeStrain collection in tabular format at 
https://www.ccug.se/collections/search?collection=typestrains. First, all the data was manually copied into 
a tab-delimited file named "Records" that can be found in the same folder as this script.
"""

def getData(i):
    url = "https://www.ccug.se/strain?id=" + str(i) + "&s=3800&p=39&sort=rel&collection=typestrains&records=100&t="
    try:
        # extract the Conditions Remarks
        dfs = pd.read_html(url)
        dict = dfs[0].set_index(0).to_dict()[1]
        infoCCUG = dict['Conditions Remarks:']
        return infoCCUG
    except KeyError:
        return "NA"
    except ValueError:
        return "NA"


def getDataAlt(i, alt):
    url = "https://www.ccug.se/strain?id=" + str(i) + "%20" + alt + "&s=0&p=1&sort=rel&collection=typestrains&records=25&t=" + str(i)
    try:
        # extract the Conditions Remarks
        dfs = pd.read_html(url)
        dict = dfs[0].set_index(0).to_dict()[1]
        infoCCUG = dict['Conditions Remarks:']
        return infoCCUG
    except KeyError:
        return "NA"
    except ValueError:
        return "NA"


if __name__ == "__main__":
    # read in the records data
    df_CCUG = pd.read_csv("Records.tsv", delimiter = "\t", header = 0, index_col=False)
    
    # open a new file named "CCUG_info2.tsv" to store the extracted growth condition data for each record
    with open("CCUG_info2.tsv","w+", encoding = "utf-16") as f:
        f.write("CCUG Number" + "\t" + "cond" + "\n")
        for record in df_CCUG['CCUG Number']:
            time.sleep(0.2)
            # remove all records containing "#" since these records are not publicly accessible
            if "#" in record: #T, A#T, B#T or !#T
                continue

            ## the URLs contain the strain IDs which are the CCUG numbers without their letter-based suffices
            # get strain ID
            i = re.search(r"([0-9]+)", record).group(1)

            try:
                # if the CCUG number contains at least two consecutive letters, use the getDataAlt function
                # extract the letter before T since this is part of the url
                alt = re.search(r"([A-Za-z!])+T",record).group(1)
                f.write(str(record) + "\t" + str(getDataAlt(i,alt)) + "\n")
                f.flush()
            except AttributeError:
                # else use the getData function
                f.write(str(record) + "\t" + str(getData(i)) + "\n")
                f.flush()
