import pandas as pd

## Script to find the maximal absolute slope, variance and range


# initialize
maxSlope = [0]*56060
maxRange = [0]*56060
maxVariance = [0]*56060

df = pd.read_csv("MetaStability_B1.tsv", sep = "\t", header = 0)
descriptions = list(df["Description"])

for col in ["K1","K2","K3","K4","K5","K6","K7","K8","K9","K10","T1","T2","T3","T4","T5","ST1","ST2","ST3","ST4","ST5","ST6",
            "ST7","ST8","B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","Z1","Z2","Z3","Z4","Z5","MSWHIM1","MSWHIM2",
            "MSWHIM3","VHSE1","VHSE2","VHSE3","VHSE4","VHSE5","VHSE6","VHSE7","VHSE8","F1","F2","F3","F4","F5","F6",
            "PP1","PP2","PP3"]:
    print(col)
    dfM = pd.read_csv("MetaStability_" + col + ".tsv", sep = "\t", header = 0)

    for i in range(0,56060):
        data_i = dfM.iloc[i,]
        if data_i["Range"] >maxRange[i]:
            maxRange[i] = data_i["Range"]
        if data_i["Slope"] >maxSlope[i]:
            maxSlope[i] = data_i["Slope"]
        if data_i["Variance"] >maxVariance[i]:
            maxVariance[i] = data_i["Variance"]

    df = pd.DataFrame({"Description":descriptions,"Range":maxRange, "Slope":maxSlope, "Variance":maxVariance})
    df.to_csv("maxSRV.tsv", sep = "\t", index= False)

