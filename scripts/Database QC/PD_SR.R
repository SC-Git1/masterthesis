# import packages
library(picante)
library(ape)
library(labdsv)
library(plyr)
library(dplyr)

# import Newick tree of all TaxIds
tree <- ape::read.tree("TreeAll.nw")

# import data
dataSub <- read.csv("Total.tsv" ,header=TRUE, sep = "\t", colClasses=c(
  "ncbiTaxID"="character", "Temp"="numeric"))

# take subset: 
# before taking a subset, randomly shuffle the dataset
# Note: manually updated seed from 1 to 10
set.seed(10)
dataSub2 <- dataSub %>% group_by(Source) %>% mutate(ncbiTaxID=sample(ncbiTaxID)) %>% top_n(100) %>% ungroup() 

# count per source (col1) and per TaxID (col2) the abundance (col3)
countsSub <- ddply(dataSub2, .(dataSub2$Source, dataSub2$ncbiTaxID), nrow)
names(countsSub) <- c("Source", "ncbiTaxID", "Freq")

# convert to a dataframe with samples as rows, taxa as columns, and abundance values for taxa in samples
dataMatSub <- labdsv::matrify(countsSub, strata = FALSE, base = 0)
pd(dataMatSub, tree, include.root = FALSE)
