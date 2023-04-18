import pandas as pd
import random
import numpy as np
import time
import re

def find_Upperlimit():
    j = -1
    random.seed(123)
    for i in np.random.randint(1, 10000, 191).tolist():
        i = int(i)
        print("i", i)
        time.sleep(1)
        result = getData(i)
        if result != "NA":
            print(i, result)
        if i > j:
            j = i
    print(j)

def getData(i):
    url = "https://mcc.nies.go.jp/strainList.do?strainId=" + str(i)
    try:
        dfs = pd.read_html(url)
        return dfs
    except KeyError:
        return "NA"
    except ValueError:
        return "NA"

if __name__ == '__main__':
  """
  find_Upperlimit() results:
  the maximum strainID was 4288
  (after running, the largest NIES number found was 4606)
  """
    with open("/content/drive/MyDrive/masterthesis/extract_NIES_StrainCorr.tsv", "w", encoding = "latin1") as f:
        f.write("Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "Source_ID" + "\n")
        for i in range(4610):
            time.sleep(0.1)
            name = ""
            temp = ""
            strain = ""
            result = getData(i)
            if (result != "NA"):
                ## select rows containing the words: "Scientific name", "Culture condition (Preculture condition)", "Strain number" (= NIES number)
                # the name consists of the first three words
                if "complex" in result[1][4][3]:
                    name = " ".join(result[1][4][3].split()[:3]).replace("*", "")
                # the name consists of the first three words
                elif "cf." in result[1][4][3]:
                    name = " ".join(result[1][4][3].split()[:3]).replace("*", "")
                else:
                # the name consists of the first two words
                    name = " ".join(result[1][4][3].split()[:2]).replace("*", "")
                source_id = result[1][4][0]
                ## Note: TODO check if some of the names are still incorrect (from previous runs)
                
                # get temperature
                try:
                    extract = re.search('.*Temperature: (.*)  Light', result[1][4][14])
                    temp = str(extract.group(1))
                except:
                    extract = re.search('.*Temperature: (.*)  L/D cycle', result[1][4][14])
                    if extract == None:
                        extract = re.search('.*Temperature: (.*)  Duration', result[1][4][14])
                    temp = str(extract.group(1))
                
                # get strain
                try:
                    extract = re.search('Other strain no. : (.*)', result[1][4][19])
                    strain = str(extract.group(1))
                except:
                    strain = ""
                
                if name != "" and temp != "":
                  strain = str(strain).replace(u"\u2212", '-').replace(u"\u2460", "1").replace(u"\u2462", "3").replace(u"\u2642", "").replace(u"\u2640", "").replace(u"\u30fb",".").replace(u"\uff26", "F")
                  f.write(name +  "\t" + strain + "\t" + str(temp) + "\t" + source_id + "\n")
                  f.flush()
