## load packages
library(phytools)
library(treeio)
library(glottoTrees)


# import data
data<-read.csv("TaxIdsProteomes.tsv",sep = "\t", header=TRUE,row.names=1)
tree <-treeio::read.newick("TreeProteomes.nw")

# create an additional row with the TaxIds and reset index
data <- cbind("Species" = rownames(data), data)
rownames(data) <- 1:nrow(data)


# tree is a phylo object with branch lengths = 1
tree <- as.phylo(tree)
tree3 <- rescale_branches(tree)

# Create named vector containing values for a single continuously distributed trait
Temps = setNames(object = data$Temp, nm = data$Species)

# ML approximation of Pagel's lambda
phylosig(tree3, Temps, method="lambda", test=TRUE, nsim=2)


