#!usr/bin/python3

#### Script to calculate range, slope and absolute variance on the proteins for each descriptor


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


if __name__ == "__main__":
    # import the data
    dfD = pd.read_csv("StabilitySubsetAA_all.csv", header = 0)


    for col in ["K2","K3","K4","K5","K6","K7","K8","K9","K10","T1","T2","T3","T4","T5","ST1","ST2","ST3","ST4","ST5",
                "ST6","ST7","ST8","B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","Z1","Z2","Z3","Z4","Z5",
                "MSWHIM1","MSWHIM2","MSWHIM3","VHSE1","VHSE2","VHSE3","VHSE4","VHSE5","VHSE6","VHSE7","VHSE8","F1",
                "F2","F3","F4","F5","F6","PP1","PP2","PP3"]:

        data = dfD[["Description", "Percentile", col]]

        # initialize
        ranges = []
        variances = []
        slopes = []
        descriptions = []

        for i in range(0, 56060):
            # with i go over each protein:
            # get the estimates for each percentage
            data_i = data.iloc[i:len(dfD):56060,:].reset_index(drop = True)
            descriptions.append(data_i["Description"][0])
            data_stable = data_i[col][69:] # top 70%
            # range
            ranges.append(max(data_stable) - min(data_stable))
            # variance
            variances.append(np.var(data_stable))
            # absolute slope
            LR  = linregress(list(range(0,31)), data_stable)
            slopes.append(abs(LR.slope))

        # store for every descriptor as a MetaStability_ file
        dfRes = pd.DataFrame({'Description': descriptions, 'Range': ranges, 'Variance': variances,'Slope':slopes})
        dfRes.to_csv("MetaStability_" + col + ".tsv", sep = "\t", index = False)

