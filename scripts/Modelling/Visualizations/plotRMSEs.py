import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Script to plot the RMSEs per temperature bin for the SVR, RF or XGboost model

# read in the RMSE vlaues
df = pd.read_csv("RMSEs.tsv", sep = "\t", header = 0)

# For the other models, replace value with "XGboost" or "SVR"

df = df[df["Model"] == "RF"]

# create the plot
g = sns.catplot(data=df, x="bin", y = "RMSE", hue="Resampling", kind = "bar",
                palette = ["skyblue", "seagreen","tomato", "silver"])

h,l = plt.gca().get_legend_handles_labels()
g._legend.remove()

g.fig.legend(h,l, ncol=4, loc = "upper center")
# plt.tight_layout()
plt.xlabel("Temperature bin [°C]")
plt.ylabel("RMSE [°C]")
plt.show()