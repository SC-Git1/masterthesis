# import packages
library(ggplot2)
library(dplyr)
library("ape")
library("ggtree")


## in working directory
# import data
data <- read.csv("Total.tsv" ,header=TRUE, sep = "\t", colClasses=c(
  "ncbiTaxID"="character", "Temp"="numeric"))

# change types
data$Temp = as.numeric(data$Temp)
data$Source = as.factor(data$Source)
data$Phylum <- as.factor(data$Phylum)
data$Superkingdom <- as.factor(data$Superkingdom)
# replace Lyubetsky et al., 2020 with its abbreviation Lyu2020
levels(data$Source) <- c("aciDB", "BacDive", "CCUG", "CECT", "Lyu2020", 
                         "MediaDB", "NCTC", "NIES", "TEMPURA", "ThermoBase")

# plot the distribution of the domains per database
dataDomain <- data[!duplicated(data[c("ncbiTaxID","Temp","Source")]),]

plotDomains <- ggplot(dataDomain, aes(x = factor(Source), fill = factor(Superkingdom, levels = c("Archaea", "Eukaryota", "Bacteria")))) +
  geom_bar(position= position_fill(reverse = TRUE), alpha = 0.8) + theme_classic(base_size = 14) +
  scale_fill_manual(name="", values = c("#DC143C","#32CD32","#2030AC")) + 
  ylab("Fraction") + xlab("Database") + 
  theme(axis.text=element_text(family = "sans", colour = "black"), 
        axis.title=element_text(family = "sans", size = 12.5 ), 
        legend.title=element_text(family = "sans"), 
        legend.text=element_text(family = "sans")) + coord_flip()

plotDomains + theme(legend.position="bottom")


# plot the distribution of the databases per domain
plotSourcesD <- ggplot(dataDomain, aes(x = factor(Superkingdom), fill = factor(Source))) +
  geom_bar(position= position_fill(reverse = TRUE), alpha = 0.8) + theme_classic(base_size = 14) +
  scale_fill_brewer(name="", palette = "Paired") + #, values = c("#DC143C","#32CD32","#2030AC")) + 
  ylab("Fraction") + xlab("Domain") + 
  theme(axis.text=element_text(family = "sans", colour = "black"), 
        axis.title=element_text(family = "sans", size = 12.5 ), 
        legend.title=element_text(family = "sans"), 
        legend.text=element_text(family = "sans")) + coord_flip()

plotSourcesD + theme(legend.position="right")

# Annotate the common culturing temperatures (CCTs)
data2 <- dataDomain %>% mutate(Status = case_when((Superkingdom == "Bacteria" & Temp == 37) ~ "Bact - 37°C", 
    (Superkingdom == "Bacteria" & Temp == 30) ~ "Bact - 30°C", (Superkingdom == "Bacteria" & Temp == 28) ~ "Bact - 28°C", 
    (Superkingdom == "Archaea" & Temp == 37) ~ "Archaea - 37°C", 
    (Phylum %in% c("Ascomycota", "Basidiomycota", "Mucoromycota", "Blastocladiomycota") & Temp %in% c(24,25,26)) ~ "Fungi",
    (Phylum %in% c("Rhodophyta", "Chlorophyta", "Haptophyta") & Temp == 20) ~ "algae"))
data2["Status"][is.na(data2["Status"])] <- "other"

# plot the fraction of CCTs
plotCCT <- ggplot(data2, aes(x = factor(Source), fill = factor(Status, 
          levels = c("Archaea - 37°C", "Bact - 28°C", "Bact - 30°C", "Bact - 37°C", "algae", "Fungi", "other")))) +
  geom_bar(position= "fill") + ylab("Fraction") +
  xlab("Database") +  scale_fill_manual("Temperature", values = c("algae" = "#aee1ae","other" = "#d3d3d3",
      "Bact - 30°C"= "#7d8ae8", "Bact - 37°C" = "#c3c9f3", "Bact - 28°C" = "#202fac",
      "Archaea - 37°C" = "#fc024c", "Fungi" = "#51c878")) +
  theme_classic() +  theme(plot.title = element_text(size = 20, hjust=0.5),axis.text=element_text(size=12, colour = "black"),
                           axis.title=element_text(size=14), legend.title=element_text(size=14), 
                           legend.text=element_text(size=12))

plotCCT + theme(legend.position="bottom")

### plot the absence-presence matrix and phylogenetic tree of the phyla present in the database

# load tree of all Phyla created with the NCBI Common Tree
tree <- read.tree("phyliptree_All_Phyla.phy")

# define the tree format
rect <- ggtree(tree, layout = "rectangular")
# add tip labels
rect$data$label <- sapply(X = rect$data$label, FUN = function(t) gsub(pattern = "\'", replacement = "", x = t, fixed = TRUE))

## create the absence-presence matrix
# intitialize
df <- data.frame(matrix(ncol = 10, nrow = 0))
colnames(df) <- levels(data$Source)

# update matrix
for (lvl in 2:length(levels(data$Phylum))) {
  for (src in levels(data$Source)) {
    if (any(subset(data, Source == src)["Phylum"]==levels(data$Phylum)[lvl])) {
      df[lvl-1, src] = "Present"
    } else {
      df[lvl-1, src] = "Absent"
    }
  }
}

# index
rownames(df) <- levels(data$Phylum)[-1]

# plot
plotPhylum <- gheatmap(rect, df, offset=2.5, width=1.2,
               colnames_angle=0, colnames_offset_y = 0, font.size = 3) +
  scale_fill_manual("", values = c("Absent" = "grey65", "Present" = "lightgreen")) + 
  geom_tiplab(size=2.5) # + geom_tippoint(aes(color=Kingdom))

plotPhylum 

